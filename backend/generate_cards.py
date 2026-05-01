import argparse
from app.db.session import SessionLocal
from app.services.card_service import CardService
from app.models.card import Card

def generate_batch(count: int, days: int):
    """
    批量生成卡密并存入数据库
    """
    db = SessionLocal()
    print(f"Generating {count} cards valid for {days} days...")
    
    try:
        created_count = 0
        for _ in range(count):
            card = CardService.create_card(db, days_valid=days)
            print(f"Created: {card.card_id}")
            created_count += 1
        
        print(f"\nSuccessfully generated {created_count} cards.")
    except Exception as e:
        print(f"Error during batch generation: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Card Generator")
    parser.add_argument("--count", type=int, default=10, help="Number of cards to generate")
    parser.add_argument("--days", type=int, default=365, help="Days until expiration")
    
    args = parser.parse_args()
    generate_batch(args.count, args.days)
