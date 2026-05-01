import os
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.card import Card, AnalysisResult
from app.core.config import settings

def cleanup_privacy_data():
    """
    清理任务：
    1. 删除 24 小时前的原始图片
    2. 物理删除已逻辑删除超过 30 天的分析结果 (可选)
    """
    db = SessionLocal()
    try:
        # 1. 清理过期图片 (24小时前)
        cutoff_time = time.time() - (24 * 3600)
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"Automatically deleted expired image: {filename}")
                    except Exception as e:
                        print(f"Error deleting file {filename}: {e}")
        
        # 2. 可以在这里添加更多清理逻辑，如过期卡密处理等
        
    finally:
        db.close()

if __name__ == "__main__":
    # 模拟定时任务运行
    print("Starting manual privacy cleanup...")
    cleanup_privacy_data()
    print("Cleanup completed.")
