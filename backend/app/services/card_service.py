import secrets
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.card import Card, CardStatus

class CardService:
    @staticmethod
    def generate_card_id() -> str:
        """
        生成16位卡密，格式：XXXX-XXXX-XXXX-XXXX
        排除易混淆字符 (0/O, 1/I/L)
        """
        chars = string.ascii_uppercase.replace('O', '').replace('I', '') + '23456789'
        card_raw = ''.join(secrets.choice(chars) for _ in range(16))
        return f"{card_raw[0:4]}-{card_raw[4:8]}-{card_raw[8:12]}-{card_raw[12:16]}"

    @classmethod
    def create_card(cls, db: Session, days_valid: int = 365) -> Card:
        """创建一张新卡密"""
        card_id = cls.generate_card_id()
        expire_at = datetime.now() + timedelta(days=days_valid)
        
        db_card = Card(
            card_id=card_id,
            expire_at=expire_at,
            status=CardStatus.NOT_ACTIVATED
        )
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return db_card

    @staticmethod
    def get_card_by_id(db: Session, card_id: str) -> Card:
        """根据卡密ID查询卡片"""
        return db.query(Card).filter(Card.card_id == card_id).first()

    @staticmethod
    def activate_card(db: Session, card: Card):
        """激活卡片"""
        card.status = CardStatus.ACTIVATED
        card.activated_at = datetime.now()
        db.commit()
        db.refresh(card)
