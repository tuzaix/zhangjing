from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings

def migrate():
    """
    手动迁移脚本：为 interpretation_caches 表添加逻辑删除字段
    """
    print(f"Connecting to database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}")
    
    add_is_deleted_sql = "ALTER TABLE interpretation_caches ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;"
    add_deleted_at_sql = "ALTER TABLE interpretation_caches ADD COLUMN deleted_at DATETIME(6) NULL;"

    with engine.connect() as conn:
        print("Adding 'is_deleted' column...")
        try:
            conn.execute(text(add_is_deleted_sql))
            conn.commit()
            print("Successfully added 'is_deleted' column.")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("Column 'is_deleted' already exists.")
            else:
                print(f"Error: {e}")

        print("Adding 'deleted_at' column...")
        try:
            conn.execute(text(add_deleted_at_sql))
            conn.commit()
            print("Successfully added 'deleted_at' column.")
        except Exception as e:
            if "Duplicate column" in str(e):
                print("Column 'deleted_at' already exists.")
            else:
                print(f"Error: {e}")

    print("Database migration completed.")

if __name__ == "__main__":
    migrate()
