import time
import json
import redis
import base64
import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from openai import OpenAI
from app.models.card import AnalysisResult, Card, CardStatus, InterpretationCache
from app.core.config import settings
from app.core import prompts

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisService:
    @staticmethod
    def get_redis_client():
        # ... (保持原样)
        try:
            return redis.Redis(
                host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT, 
                db=0,
                decode_responses=True
            )
        except Exception:
            return None

    @staticmethod
    def get_openai_client():
        if settings.OPENAI_API_KEY == "your-openai-api-key":
            return None
        return OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )

    @classmethod
    def analyze_with_vision_model(cls, image_path: str, right_image_path: str, mode: str = "standard", model: str = None):
        """
        调用支持视觉的 AI 模型进行分析 (支持 GPT-4o, Claude 3.5 Sonnet 等)
        强制要求双手对比分析
        """
        client = cls.get_openai_client()
        if not client:
            logger.error("AI client not initialized. Check API Key.")
            return None

        # 使用传入的模型，或者配置文件中的默认模型
        target_model = model or settings.DEFAULT_MODEL
        logger.info(f"Starting AI analysis with model: {target_model}, mode: {mode}")

        try:
            # 准备图片内容
            content_list = []
            
            # 加载左手
            with open(image_path, "rb") as f:
                left_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # 加载右手
            if not right_image_path or not os.path.exists(right_image_path):
                logger.error("Right hand image missing for dual-hand analysis.")
                return None
                
            with open(right_image_path, "rb") as f:
                right_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # 从配置文件加载 Prompt
            system_role = prompts.SYSTEM_ROLE
            mode_desc = prompts.MODES_CONFIG.get(mode, prompts.MODES_CONFIG["standard"])
            
            # 双手分析模式
            user_prompt = prompts.ANALYSIS_PROMPT_TEMPLATE_DUAL.format(mode_desc=mode_desc)
            
            content_list.append({"type": "text", "text": user_prompt})
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{left_base64}", "detail": "high"}
            })
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{right_base64}", "detail": "high"}
            })

            # 准备消息内容
            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": content_list}
            ]

            # 准备请求参数
            params = {
                "model": target_model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 8192
            }

            if "gpt" in target_model.lower():
                params["response_format"] = { "type": "json_object" }

            response = client.chat.completions.create(**params)
            content = response.choices[0].message.content
            logger.info(f"AI Response received from {target_model}")

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                logger.error(f"Failed to parse AI response as JSON: {content}")
                return None

        except Exception as e:
            logger.error(f"AI API Error ({target_model}): {e}")
            return None

    @classmethod
    def run_analysis(cls, db: Session, card_id: str, mode: str = "standard", image_path: str = None, model: str = None, right_image_path: str = None):
        """执行AI analysis逻辑，支持数据库持久化缓存"""
        # 0. 检查卡片状态
        card = db.query(Card).filter(Card.card_id == card_id).first()
        if not card or card.status == CardStatus.USED:
            logger.warning(f"Card {card_id} is not valid or already used.")
            return None

        # 0. 首先检查数据库中是否存在该模式的缓存 (且未被逻辑删除)
        cached_interpretation = db.query(InterpretationCache).filter(
            InterpretationCache.card_id == card_id,
            InterpretationCache.mode == mode,
            InterpretationCache.is_deleted == False
        ).first()
        
        if cached_interpretation:
            logger.info(f"Returning DB cached result for card: {card_id}, mode: {mode}")
            return cached_interpretation.result_json

        if not image_path or not os.path.exists(image_path) or not right_image_path or not os.path.exists(right_image_path):
            logger.warning(f"Both hand images must be provided and exist for card: {card_id}")
            return None

        result_data = cls.analyze_with_vision_model(image_path, right_image_path, mode=mode, model=model)
        
        # 如果分析失败（返回 None），则直接返回
        if not result_data:
            logger.error(f"AI analysis failed for card: {card_id}")
            return None
        
        # 1. 保存到数据库 (InterpretationCache)
        new_cache = InterpretationCache(
            card_id=card_id,
            mode=mode,
            result_json=result_data
        )
        db.add(new_cache)
        
        # 2. 如果是标准模式或第一次分析，同步更新到 AnalysisResult 主表
        db_result = db.query(AnalysisResult).filter(AnalysisResult.card_id == card_id).first()
        if not db_result:
            db_result = AnalysisResult(
                card_id=card_id,
                result_json=result_data
            )
            db.add(db_result)
        elif mode == "standard":
            db_result.result_json = result_data
        
        # 3. 更新卡片状态
        card = db.query(Card).filter(Card.card_id == card_id).first()
        if card:
            card.status = CardStatus.ACTIVATED
            if not card.activated_at:
                card.activated_at = datetime.now()
        
        db.commit()

        # 4. Redis 仅用于全局热点数据的临时缓存预热
        redis_client = cls.get_redis_client()
        if redis_client:
            cache_key = f"analysis:hot_result:{card_id}:{mode}"
            redis_client.setex(
                cache_key,
                3600,  # 热点缓存 1 小时
                json.dumps(result_data, ensure_ascii=False)
            )

        return result_data

    @classmethod
    def get_result(cls, db: Session, card_id: str, mode: str = "standard"):
        """获取已生成的分析结果，优先从数据库缓存表读取"""
        # 1. 尝试从 Redis 热点缓存读取 (可选)
        redis_client = cls.get_redis_client()
        if redis_client:
            cache_key = f"analysis:hot_result:{card_id}:{mode}"
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

        # 1. 记录查看统计
        db_result = db.query(AnalysisResult).filter(
            AnalysisResult.card_id == card_id,
            AnalysisResult.is_deleted == False
        ).first()
        if db_result:
            db_result.view_count += 1
            db_result.last_view_at = datetime.now()
            db.commit()

        # 2. 从 InterpretationCache 数据库表读取 (核心优化：模式结果持久化)
        cached_interpretation = db.query(InterpretationCache).filter(
            InterpretationCache.card_id == card_id,
            InterpretationCache.mode == mode,
            InterpretationCache.is_deleted == False
        ).first()
        
        if cached_interpretation:
            # 写入 Redis 热点缓存预热
            if redis_client:
                cache_key = f"analysis:hot_result:{card_id}:{mode}"
                redis_client.setex(cache_key, 3600, json.dumps(cached_interpretation.result_json, ensure_ascii=False))
            return cached_interpretation.result_json

        # 3. 兜底：如果缓存表没有，尝试从主表读取 (兼容旧数据)
        db_result = db.query(AnalysisResult).filter(
            AnalysisResult.card_id == card_id,
            AnalysisResult.is_deleted == False
        ).first()
        if db_result:
            return db_result.result_json
            
        return None
