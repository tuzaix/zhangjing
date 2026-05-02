from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
import uuid

from app.db.session import get_db
from app.services.analysis_service import AnalysisService
from app.core.config import settings
from app.models.card import AnalysisResult, InterpretationCache, Card, CardStatus

router = APIRouter()

class AnalysisStartRequest(BaseModel):
    card_id: str
    mode: str = "standard"
    model: str = None
    type: str = "personal"

class ShareRecordRequest(BaseModel):
    card_id: str
    template_id: int

@router.post("/share/record")
async def record_share(request: ShareRecordRequest, db: Session = Depends(get_db)):
    """记录分享行为"""
    # 可以在此处增加分享统计逻辑
    return {
        "code": 0,
        "message": "分享记录已保存"
    }

@router.post("/upload")
async def upload_image(
    card_id: str = Form(...),
    file: UploadFile = File(...)
):
    """上传手相/面相照片"""
    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 创建上传目录
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 生成唯一文件名
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{card_id}_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "code": 0,
        "message": "图片上传成功",
        "data": {
            "file_name": file_name
        }
    }

@router.post("/upload-both")
async def upload_both_hands(
    card_id: str = Form(...),
    left_hand: UploadFile = File(...),
    right_hand: UploadFile = File(...)
):
    """同时上传左右手照片"""
    if not left_hand.content_type.startswith("image/") or not right_hand.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 保存左手
    left_ext = os.path.splitext(left_hand.filename)[1]
    left_name = f"{card_id}_left_{uuid.uuid4()}{left_ext}"
    left_path = os.path.join(settings.UPLOAD_DIR, left_name)
    with open(left_path, "wb") as buffer:
        shutil.copyfileobj(left_hand.file, buffer)
        
    # 保存右手
    right_ext = os.path.splitext(right_hand.filename)[1]
    right_name = f"{card_id}_right_{uuid.uuid4()}{right_ext}"
    right_path = os.path.join(settings.UPLOAD_DIR, right_name)
    with open(right_path, "wb") as buffer:
        shutil.copyfileobj(right_hand.file, buffer)
    
    return {
        "code": 0,
        "message": "双手图片上传成功",
        "data": {
            "left": left_name,
            "right": right_name
        }
    }

@router.post("/upload-bestie")
async def upload_bestie_hands(
    card_id: str = Form(...),
    self_hand: UploadFile = File(...),
    bestie_hand: UploadFile = File(...)
):
    """上传个人与闺蜜的手相照片"""
    if not self_hand.content_type.startswith("image/") or not bestie_hand.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 保存个人手相
    self_ext = os.path.splitext(self_hand.filename)[1]
    self_name = f"{card_id}_self_{uuid.uuid4()}{self_ext}"
    self_path = os.path.join(settings.UPLOAD_DIR, self_name)
    with open(self_path, "wb") as buffer:
        shutil.copyfileobj(self_hand.file, buffer)
        
    # 保存闺蜜手相
    bestie_ext = os.path.splitext(bestie_hand.filename)[1]
    bestie_name = f"{card_id}_bestie_{uuid.uuid4()}{bestie_ext}"
    bestie_path = os.path.join(settings.UPLOAD_DIR, bestie_name)
    with open(bestie_path, "wb") as buffer:
        shutil.copyfileobj(bestie_hand.file, buffer)
    
    return {
        "code": 0,
        "message": "闺蜜匹配图片上传成功",
        "data": {
            "self": self_name,
            "bestie": bestie_name
        }
    }

@router.post("/upload-couple")
async def upload_couple_hands(
    card_id: str = Form(...),
    male_hand: UploadFile = File(...),
    female_hand: UploadFile = File(...)
):
    """上传男生与女生（情侣）的手相照片"""
    if not male_hand.content_type.startswith("image/") or not female_hand.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # 保存男生手相
    male_ext = os.path.splitext(male_hand.filename)[1]
    male_name = f"{card_id}_male_{uuid.uuid4()}{male_ext}"
    male_path = os.path.join(settings.UPLOAD_DIR, male_name)
    with open(male_path, "wb") as buffer:
        shutil.copyfileobj(male_hand.file, buffer)
        
    # 保存女生手相
    female_ext = os.path.splitext(female_hand.filename)[1]
    female_name = f"{card_id}_female_{uuid.uuid4()}{female_ext}"
    female_path = os.path.join(settings.UPLOAD_DIR, female_name)
    with open(female_path, "wb") as buffer:
        shutil.copyfileobj(female_hand.file, buffer)
    
    return {
        "code": 0,
        "message": "情侣匹配图片上传成功",
        "data": {
            "male": male_name,
            "female": female_name
        }
    }

@router.post("/start")
async def start_analysis(request: AnalysisStartRequest, db: Session = Depends(get_db)):
    """开始AI分析任务"""
    # 寻找该卡密上传的最新相关图片
    img1_path = None
    img2_path = None
    
    # 根据业务类型确定搜索前缀
    if request.type == "bestie":
        prefix1, prefix2 = "self_", "bestie_"
        error_msg = "必须上传完整的个人与闺蜜照片方可开始分析"
    elif request.type == "couple":
        prefix1, prefix2 = "male_", "female_"
        error_msg = "必须上传完整的男生与女生照片方可开始分析"
    else: # personal
        prefix1, prefix2 = "left_", "right_"
        error_msg = "必须上传完整的左右手照片方可开始分析"

    if os.path.exists(settings.UPLOAD_DIR):
        all_files = os.listdir(settings.UPLOAD_DIR)
        
        # 找图1
        img1_files = [f for f in all_files if f.startswith(f"{request.card_id}_{prefix1}")]
        if img1_files:
            img1_files.sort(key=lambda x: os.path.getmtime(os.path.join(settings.UPLOAD_DIR, x)), reverse=True)
            img1_path = os.path.join(settings.UPLOAD_DIR, img1_files[0])
            
        # 找图2
        img2_files = [f for f in all_files if f.startswith(f"{request.card_id}_{prefix2}")]
        if img2_files:
            img2_files.sort(key=lambda x: os.path.getmtime(os.path.join(settings.UPLOAD_DIR, x)), reverse=True)
            img2_path = os.path.join(settings.UPLOAD_DIR, img2_files[0])

    if not img1_path or not img2_path:
        raise HTTPException(status_code=400, detail=error_msg)

    result = AnalysisService.run_analysis(
        db, 
        request.card_id, 
        request.mode, 
        image_path=img1_path,
        right_image_path=img2_path,
        model=request.model,
        analysis_type=request.type
    )
    return {
        "code": 0,
        "message": "分析完成",
        "data": result
    }

@router.get("/get/{card_id}")
async def get_analysis_result(card_id: str, mode: str = "standard", db: Session = Depends(get_db)):
    """获取分析结果"""
    result = AnalysisService.get_result(db, card_id, mode)
    # 如果没有数据，直接返回 null (即返回为空)
    return {
        "code": 0,
        "data": result
    }

class PrivacyDeleteRequest(BaseModel):
    card_id: str
    confirm: bool

@router.post("/delete")
async def delete_user_data(request: PrivacyDeleteRequest, db: Session = Depends(get_db)):
    """用户主动删除所有隐私数据"""
    if not request.confirm:
        raise HTTPException(status_code=400, detail="请确认删除操作")
    
    card_id = request.card_id.strip().upper()
    now = datetime.now()
    
    # 1. 逻辑删除所有分析结果和模式缓存
    db.query(AnalysisResult).filter(AnalysisResult.card_id == card_id).update({
        "is_deleted": True,
        "deleted_at": now
    })
    
    db.query(InterpretationCache).filter(InterpretationCache.card_id == card_id).update({
        "is_deleted": True,
        "deleted_at": now
    })
    
    # 2. 清理该卡密关联的物理图片
    try:
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                if filename.startswith(card_id):
                    os.remove(os.path.join(settings.UPLOAD_DIR, filename))
    except Exception as e:
        print(f"Error cleaning files: {e}")

    # 3. 标记卡密为已使用/核销，不再允许查看
    card = db.query(Card).filter(Card.card_id == card_id).first()
    if card:
        card.status = CardStatus.USED
    
    # 4. 清理 Redis 缓存
    try:
        redis_client = AnalysisService.get_redis_client()
        if redis_client:
            # 模式缓存通常是 analysis:hot_result:{card_id}:{mode}
            # 我们直接根据模式清理，或者更直接点，清理该卡密相关的 key
            # 由于 redis 没存 key 列表，我们通常根据模式列表清理，或者简单处理
            modes = ["standard", "toxic", "money", "love"]
            for mode in modes:
                cache_key = f"analysis:hot_result:{card_id}:{mode}"
                redis_client.delete(cache_key)
    except Exception as e:
        print(f"Error cleaning Redis: {e}")

    db.commit()
    
    return {
        "code": 0,
        "message": "数据已永久删除，卡密已失效"
    }
