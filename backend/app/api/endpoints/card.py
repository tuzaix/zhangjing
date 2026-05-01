from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import re

from app.db.session import get_db
from app.services.card_service import CardService
from app.services.security_service import security_service
from app.models.card import CardStatus

router = APIRouter()

class CardVerifyRequest(BaseModel):
    card_id: str

@router.post("/verify")
def verify_card(request: CardVerifyRequest, fastapi_request: Request, db: Session = Depends(get_db)):
    ip_address = fastapi_request.client.host
    card_id = request.card_id.strip().upper()
    
    # 1. 防暴力破解检查
    if security_service.is_rate_limited(ip_address):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"code": 1005, "message": "请求过于频繁，1小时内错误尝试过多，请稍后再试"}
        )

    # 2. 格式校验
    if not re.match(r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$', card_id):
        security_service.log_attempt(ip_address, False)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1001, "message": "卡密格式错误"}
        )
    
    # 3. 查找卡片
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        security_service.log_attempt(ip_address, False)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 1002, "message": "卡密不存在"}
        )
    
    # 4. 检查是否过期
    if card.expire_at < datetime.now():
        card.status = CardStatus.EXPIRED
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1003, "message": "卡密已过期"}
        )
    
    # 5. 根据状态返回
    if card.status == CardStatus.NOT_ACTIVATED:
        return {
            "code": 0,
            "status": "not_activated",
            "message": "卡密验证成功，请上传图片",
            "data": {
                "expire_at": card.expire_at.isoformat()
            }
        }
    elif card.status == CardStatus.ACTIVATED:
        return {
            "code": 0,
            "status": "activated",
            "message": "找到分析报告",
            "data": {
                "activated_at": card.activated_at.isoformat() if card.activated_at else None
            }
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1004, "message": "该卡密已被核销或已使用"}
        )

# 仅供开发调试使用的接口：创建测试卡密
@router.post("/create-test", include_in_schema=False)
def create_test_card(db: Session = Depends(get_db)):
    card = CardService.create_card(db)
    return {"card_id": card.card_id}
