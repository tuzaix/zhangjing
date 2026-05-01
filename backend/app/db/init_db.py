from app.db.session import engine, Base
from app.models.card import Card, AnalysisResult
from app.core.config import settings

def init_db():
    """
    初始化数据库表结构
    """
    print(f"Connecting to database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}")
    try:
        # 创建所有定义的表
        Base.metadata.create_all(bind=engine)
        print("Successfully created all database tables.")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
