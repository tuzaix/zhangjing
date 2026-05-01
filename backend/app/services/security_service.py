import redis
from app.core.config import settings
import time

class SecurityService:
    def __init__(self):
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT, 
                db=0,
                decode_responses=True
            )
        except Exception:
            self.redis = None
            print("Warning: Redis not available, rate limiting disabled.")

    def is_rate_limited(self, ip_address: str) -> bool:
        """检查IP是否被限流 (1小时内超过5次尝试)"""
        if not self.redis:
            return False
            
        key = f"ratelimit:card_verify:{ip_address}"
        attempts = self.redis.get(key)
        
        if attempts and int(attempts) >= settings.RATE_LIMIT_MAX_ATTEMPTS:
            return True
        return False

    def log_attempt(self, ip_address: str, success: bool):
        """记录尝试，如果失败则增加计数"""
        if not self.redis or success:
            return
            
        key = f"ratelimit:card_verify:{ip_address}"
        self.redis.incr(key)
        # 第一次失败时设置过期时间
        if int(self.redis.get(key)) == 1:
            self.redis.expire(key, settings.RATE_LIMIT_WINDOW_SECONDS)

security_service = SecurityService()
