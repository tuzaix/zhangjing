from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import csv
import io

from app.db.session import get_db
from app.models.card import Card, CardStatus, AnalysisResult, InterpretationCache
from app.services.card_service import CardService
from app.core.config import settings

router = APIRouter()

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class CardCreateRequest(BaseModel):
    count: int = 10
    days_valid: int = 365

class CardResponse(BaseModel):
    card_id: str
    status: str
    created_at: datetime
    expire_at: datetime
    activated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PaginatedCardsResponse(BaseModel):
    total: int
    items: List[CardResponse]

@router.post("/login")
async def admin_login(request: AdminLoginRequest):
    if request.username == settings.ADMIN_USERNAME and request.password == settings.ADMIN_PASSWORD:
        return {"token": settings.ADMIN_SECRET_TOKEN}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="用户名或密码错误"
    )

def verify_admin(token: str = Query(...)):
    if token != settings.ADMIN_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未授权访问"
        )
    return True

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db), _: bool = Depends(verify_admin)):
    total_cards = db.query(Card).count()
    activated_cards = db.query(Card).filter(Card.status == CardStatus.ACTIVATED).count()
    not_activated_cards = db.query(Card).filter(Card.status == CardStatus.NOT_ACTIVATED).count()
    used_cards = db.query(Card).filter(Card.status == CardStatus.USED).count()
    expired_cards = db.query(Card).filter(Card.status == CardStatus.EXPIRED).count()
    
    total_analyses = db.query(AnalysisResult).count()
    total_modes_cached = db.query(InterpretationCache).count()
    
    # 模式分布统计
    mode_distribution = db.query(
        InterpretationCache.mode, 
        func.count(InterpretationCache.id)
    ).group_by(InterpretationCache.mode).all()
    
    return {
        "cards": {
            "total": total_cards,
            "activated": activated_cards,
            "not_activated": not_activated_cards,
            "used": used_cards,
            "expired": expired_cards
        },
        "analyses": {
            "total_users": total_analyses,
            "total_interpretations": total_modes_cached,
            "mode_stats": {mode: count for mode, count in mode_distribution}
        }
    }

@router.get("/cards", response_model=PaginatedCardsResponse)
async def list_cards(
    skip: int = 0, 
    limit: int = 20, 
    status: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db), 
    _: bool = Depends(verify_admin)
):
    query = db.query(Card)
    if status:
        query = query.filter(Card.status == status)
    
    total = query.count()
    
    # 动态排序
    sort_attr = getattr(Card, sort_by, Card.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_attr.desc())
    else:
        query = query.order_by(sort_attr.asc())
        
    items = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": items
    }

@router.get("/cards/export")
async def export_cards(
    status: Optional[str] = None,
    db: Session = Depends(get_db), 
    _: bool = Depends(verify_admin)
):
    query = db.query(Card)
    if status:
        query = query.filter(Card.status == status)
    
    cards = query.order_by(Card.created_at.desc()).all()
    
    # 创建内存 CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头 (BOM for Excel)
    output.write('\ufeff')
    writer.writerow(['卡密ID', '状态', '创建时间', '激活时间', '过期时间'])
    
    for card in cards:
        writer.writerow([
            card.card_id,
            card.status,
            card.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            card.activated_at.strftime('%Y-%m-%d %H:%M:%S') if card.activated_at else '-',
            card.expire_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    filename = f"cards_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/cards/generate")
async def generate_cards(
    request: CardCreateRequest, 
    db: Session = Depends(get_db), 
    _: bool = Depends(verify_admin)
):
    cards = []
    for _ in range(request.count):
        card = CardService.create_card(db, days_valid=request.days_valid)
        cards.append(card.card_id)
    return {"count": len(cards), "cards": cards}

@router.get("/interactions")
async def list_interactions(
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db), 
    _: bool = Depends(verify_admin)
):
    results = db.query(AnalysisResult).order_by(AnalysisResult.created_at.desc()).offset(skip).limit(limit).all()
    return [{
        "card_id": r.card_id,
        "created_at": r.created_at,
        "view_count": r.view_count,
        "last_view_at": r.last_view_at
    } for r in results]
