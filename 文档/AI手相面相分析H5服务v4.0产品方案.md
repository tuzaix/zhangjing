# AI手相面相分析H5服务v4\.0产品方案

## v4\.0 版本

---

## 文档信息

|项目|内容|
|---|---|
|产品名称|AI 手相面相分析 H5 服务|
|版本号|v4\.0|
|上次更新|2026\-05\-01|
|文档状态|正式发布|
|主要更新|卡密支付系统优化、数据缓存机制升级、隐私保护机制增强|

---

## 第 1 章 产品概述

### 1\.1 产品定位

AI 手相面相分析 H5 服务是一款基于人工智能技术的命理分析工具，用户通过上传手相或面相照片，即可获得专业的 AI 分析报告。产品采用卡密支付模式，无需注册登录，最大限度保护用户隐私。

### 1\.2 核心价值

- **隐私优先**：无账号体系，卡密作为唯一标识

- **便捷支付**：卡密模式简化支付流程

- **快速体验**：缓存机制确保二次查看秒级响应

- **数据安全**：自动清理机制保障用户数据安全

### 1\.3 v4\.0 版本升级要点

1. 卡密系统核心逻辑优化，完善状态流转机制

2. 多级缓存架构升级，提升系统性能

3. 隐私保护机制增强，数据匿名化处理

4. 用户体验全面优化，智能卡密输入

5. 合规体系完善，满足数据安全法规要求

---

## 第 2 章 产品架构设计

### 2\.1 系统架构图

```Plain Text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户端H5      │    │   负载均衡      │    │   API网关       │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        应用服务层                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ 卡密验证 │  │ 图片上传 │  │ AI分析   │  │ 结果查询 │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                        数据层                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Redis    │  │ MySQL    │  │ 对象存储 │  │ AI引擎   │         │
│  │ 缓存     │  │ 数据库   │  │ (图片)   │  │ 服务     │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### 2\.2 核心模块划分

1. **卡密管理模块**：卡密生成、验证、状态管理

2. **图片处理模块**：上传、压缩、临时存储、自动删除

3. **AI 分析模块**：调用 AI 引擎、结果生成、数据绑定

4. **缓存管理模块**：多级缓存、数据预热、过期管理

5. **隐私保护模块**：数据清理、匿名化、合规审计

6. **用户交互模块**：页面展示、状态提示、分享功能

---

## 第 3 章 功能详细设计

### 3\.1 卡密系统核心逻辑

#### 3\.1\.1 卡密生命周期设计

**卡密状态流转图**：

```Plain Text
生成卡密
    ↓
未激活 → 已激活（绑定分析结果）→ 已核销（已查看）→ 已过期
    ↓         ↓                    ↓
用户输入   绑定结果              无法使用
    ↓
检查状态：
• 未激活 → 引导上传图片 → AI分析 → 绑定结果 → 展示结果
• 已激活 → 直接从缓存读取并展示结果
• 已核销 → 提示"该卡密已被使用"
• 已过期 → 提示"该卡密已过期"
```

**状态定义说明**：

|状态|说明|可执行操作|
|---|---|---|
|未激活|卡密已生成但未使用|验证通过，引导上传图片|
|已激活|已绑定分析结果但未查看或正在查看|直接展示分析结果|
|已核销|已完成查看流程|提示已使用，引导购买新卡密|
|已过期|超过有效期（1 年）|提示已过期，引导购买新卡密|

#### 3\.1\.2 卡密生成规则

- 格式：4 组 4 位字符，使用连字符分隔

- 示例：`ABCD\-1234\-EFGH\-5678`

- 字符集：大写字母 A\-Z \+ 数字 0\-9，排除易混淆字符（0/O, 1/I/L）

- 实际字符集：`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`

- 总组合数：32^16 ≈ 2^80，理论上无法暴力枚举

**卡密生成代码示例**：

```python
import secrets
import string

def generate_card_id():
    """生成16位卡密，格式：XXXX-XXXX-XXXX-XXXX"""
    # 排除易混淆字符
    chars = string.ascii_uppercase.replace('O', '').replace('I', '').replace('L', '') + '23456789'
    
    # 生成16位随机字符
    card_raw = ''.join(secrets.choice(chars) for _ in range(16))
    
    # 格式化为4组
    card_id = f"{card_raw[0:4]}-{card_raw[4:8]}-{card_raw[8:12]}-{card_raw[12:16]}"
    
    return card_id
```

### 3\.2 卡密输入页核心逻辑

#### 3\.2\.1 页面加载流程

1. 用户输入 16 位卡密，点击 \&\#34;验证\&\#34;

2. 后端查询卡密状态

3. 根据状态分支处理

**分支 A：卡密未激活（首次使用）**

- 提示：\&\#34;✅ 卡密验证成功！这是一张全新的分析卡\&\#34;

- 自动跳转到上传页面

- 卡密 ID 自动带入，用户无需再次输入

- 上传完成后，分析结果与该卡密永久绑定

**分支 B：卡密已激活（有缓存结果）**

- 提示：\&\#34;✅ 找到你的分析报告！\&\#34;

- 直接跳转到结果展示页

- **无需重新上传图片，无需重新调用 AI**

- 从数据库 / 缓存直接读取已生成的报告

**分支 C：卡密已核销 / 过期**

- 提示：\&\#34;❌ 该卡密已被使用或已过期\&\#34;

- 提供 \&\#34;购买新卡密\&\#34; 按钮

- 推荐分销活动：\&\#34;邀请好友免费获得卡密\&\#34;

### 3\.3 隐私保护机制设计

#### 3\.3\.1 数据存储隐私保护

**图片存储策略**：

- 用户上传的原始图片：**24 小时后自动永久删除**

- 仅保留 AI 分析后的结构化数据（JSON 格式）

- 图片不与用户身份绑定，仅与卡密 ID 关联

- 图片存储路径加密，无法直接遍历

**图片存储路径设计**：

```python
def generate_image_path(card_id):
    """生成加密的图片存储路径"""
    import hashlib
    import time
    
    # 使用卡密ID + 时间戳生成不可逆哈希
    path_hash = hashlib.sha256(f"{card_id}{time.time()}".encode()).hexdigest()
    
    # 分级目录存储，避免单目录文件过多
    return f"uploads/{path_hash[0:2]}/{path_hash[2:4]}/{path_hash}.jpg"
```

**分析数据存储结构**：

```json
{
  "card_id": "ABCD-1234-EFGH-5678",  // 仅用卡密ID关联
  "analysis_result": {
    "summary": {
      "overall_score": 85,
      "personality": "..."
    },
    "left_hand": {...},
    "right_hand": {...},
    "face": {...}
  },
  "created_at": "2026-05-01T12:00:00",
  "expire_at": "2027-05-01T12:00:00",  // 数据保留1年
  "view_count": 3,                    // 查看次数统计
  "last_view_at": "2026-05-02T15:30:00"
  // 🔴 绝对不存储：用户ID、手机号、微信OpenID、IP地址
}
```

#### 3\.3\.2 用户身份匿名化

**无账号体系设计**：

- 整个系统**不需要用户注册、不需要登录**

- 不需要手机号、不需要微信授权

- 唯一标识就是 16 位卡密

- 用户只要记住自己的卡密，随时可以查看结果

**数据隔离**：

- 不同卡密的数据完全隔离

- 无法通过卡密反推用户身份

- 后台管理系统也无法查看用户真实身份

- 数据库查询必须携带卡密 ID，无全局列表接口

#### 3\.3\.3 数据自动清理机制

**自动清理任务**：

```python
# 每日凌晨执行清理任务
def cleanup_privacy_data():
    """隐私数据自动清理任务，每日凌晨2点执行"""
    
    # 1. 删除24小时前上传的原始图片
    delete_old_images(hours=24)
    
    # 2. 删除1年前的分析结果数据
    delete_old_analysis(years=1)
    
    # 3. 删除过期卡密的所有关联数据
    delete_expired_card_data()
    
    # 4. 清理日志中的敏感信息
    sanitize_logs()
    
    # 5. 记录清理审计日志
    log_cleanup_statistics()

def delete_old_images(hours=24):
    """删除指定时间前的原始图片"""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    # 查询需要删除的图片记录
    images_to_delete = ImageUpload.objects.filter(
        created_at__lt=cutoff_time,
        is_deleted=False
    )
    
    for image in images_to_delete:
        # 删除物理文件
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        # 标记为已删除
        image.is_deleted = True
        image.save()

def sanitize_logs():
    """清理日志中的敏感信息"""
    # 移除日志中的完整卡密，只保留前4后4
    # 移除日志中的IP地址
    # 移除日志中的任何可能的个人信息
    pass
```

**用户主动删除**：

- 结果页提供 \&\#34;删除我的数据\&\#34; 按钮

- 点击后立即删除该卡密关联的所有数据

- 提示：\&\#34;数据已永久删除，无法恢复\&\#34;

- 删除后该卡密失效，无法再次查看

- 删除操作不可撤销，需二次确认

### 3\.4 用户体验优化

#### 3\.4\.1 卡密输入页体验

**智能卡密输入**：

- 4 组 4 位输入框，自动跳格

- 支持粘贴 16 位卡号，自动拆分到 4 个输入框

- 实时格式校验，输入错误即时提示

- 支持大小写不敏感

**前端输入框实现示例**：

```javascript
// 智能卡密输入组件
class CardInput {
    constructor(container) {
        this.inputs = container.querySelectorAll('.card-input');
        this.initEvents();
    }
    
    initEvents() {
        this.inputs.forEach((input, index) => {
            // 输入自动跳格
            input.addEventListener('input', (e) => {
                if (e.target.value.length === 4 && index < 3) {
                    this.inputs[index + 1].focus();
                }
                this.validateFormat();
            });
            
            // 退格回跳
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && e.target.value.length === 0 && index > 0) {
                    this.inputs[index - 1].focus();
                }
            });
        });
        
        // 支持粘贴自动拆分
        container.addEventListener('paste', (e) => {
            e.preventDefault();
            const text = (e.clipboardData || window.clipboardData).getData('text');
            this.fillCardId(text.replace(/[^A-Za-z0-9]/g, '').toUpperCase());
        });
    }
    
    fillCardId(fullCardId) {
        // 将16位卡号拆分到4个输入框
        for (let i = 0; i < 4; i++) {
            this.inputs[i].value = fullCardId.substr(i * 4, 4);
        }
    }
}
```

**历史卡密记录**：

- 本地存储（LocalStorage）记录用户使用过的卡密

- 输入框下方显示 \&\#34;最近使用的卡密\&\#34; 列表

- 点击即可快速填入

- **仅存储在用户本地，不上传到服务器**

#### 3\.4\.2 状态提示文案优化

**未激活卡密提示**：

> ✅ 卡密验证成功！
> 
> 🎉 这是一张全新的分析卡
> 
> 接下来请上传你的手相 / 面相照片
> AI 将为你生成专属深度分析报告
> 
> 

**已激活卡密（有缓存）提示**：

> ✅ 找到你的分析报告！
> 
> 📄 报告生成时间：2026\-05\-01 14:30
> 👀 已查看 3 次
> 
> 正在加载你的报告\.\.\.
> 
> 

**隐私保护提示（所有页面显示）**：

> 🔒 你的隐私我们非常重视
> 
> ・原始图片 24 小时后自动删除
> ・不收集任何个人身份信息
> ・支持随时永久删除所有数据
> ・数据仅与你的卡密绑定
> 
> 

#### 3\.4\.3 分享与二次查看

**分享卡片优化**：

- 分享卡片上只显示卡密的前 8 位 \+ 后 4 位，中间 4 位用 \\*\\*\\*\\* 隐藏

- 示例：`ABCD\-\*\*\*\*\-\*\*\*\*\-5678`

- 防止他人通过分享截图盗用卡密

- 用户可以选择 \&\#34;分享时隐藏卡密\&\#34;

**分享卡片卡密脱敏函数**：

```javascript
function maskCardId(cardId) {
    // ABCD-1234-EFGH-5678 -> ABCD-****-****-5678
    const parts = cardId.split('-');
    return `${parts[0]}-****-****-${parts[3]}`;
}
```

**二次查看引导**：

- 结果页顶部醒目提示：

    > 💡 请记住你的卡密：`ABCD\-1234\-EFGH\-5678`
    > 下次输入卡密即可直接查看结果，无需重新上传
    > 
    > 

- 提供 \&\#34;复制卡密\&\#34; 按钮

- 提供 \&\#34;保存卡密到备忘录\&\#34; 功能

- 首次查看结果时强制弹出卡密确认弹窗

---

## 第 4 章 前端页面设计

### 4\.1 页面流程

```Plain Text
卡密输入页 → 图片上传页 → AI分析中 → 结果展示页
     ↑                        ↑
     └────────────────────────┘
          输入已激活卡密直接跳转
```

### 4\.2 核心页面组件

1. **卡密输入组件**：智能输入、历史记录、格式校验

2. **图片上传组件**：拍照 / 相册选择、裁剪预览、压缩

3. **加载动画组件**：AI 分析进度展示

4. **结果展示组件**：报告渲染、折叠展开、分享

5. **隐私设置组件**：数据删除、隐私说明

---

## 第 5 章 数据库设计

### 5\.1 核心数据表

**卡密表 \(cards\)**

```sql
CREATE TABLE cards (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    card_id VARCHAR(20) UNIQUE NOT NULL COMMENT '卡密ID',
    status ENUM('not_activated', 'activated', 'used', 'expired') DEFAULT 'not_activated',
    card_token VARCHAR(64) COMMENT '上传绑定令牌',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    activated_at DATETIME NULL COMMENT '激活时间',
    expire_at DATETIME NOT NULL COMMENT '过期时间',
    INDEX idx_card_id (card_id),
    INDEX idx_status (status),
    INDEX idx_expire_at (expire_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**分析结果表 \(analysis\_results\)**

```sql
CREATE TABLE analysis_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    card_id VARCHAR(20) UNIQUE NOT NULL,
    result_json JSON NOT NULL COMMENT '分析结果JSON',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    view_count INT DEFAULT 0,
    last_view_at DATETIME NULL,
    is_deleted TINYINT DEFAULT 0,
    deleted_at DATETIME NULL,
    INDEX idx_card_id (card_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**图片上传记录表 \(image\_uploads\)**

```sql
CREATE TABLE image_uploads (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    card_id VARCHAR(20) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) COMMENT '文件哈希',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT DEFAULT 0,
    deleted_at DATETIME NULL,
    INDEX idx_card_id (card_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 第 6 章 技术实现方案

### 6\.1 多级缓存架构

#### 6\.1\.1 缓存架构设计

```Plain Text
用户输入卡密
    ↓
Redis缓存查询（1小时内热门卡密）
    ↓ 命中 → 直接返回结果
    ↓ 未命中
MySQL数据库查询
    ↓ 命中 → 写入Redis缓存，返回结果
    ↓ 未命中
卡密未激活，引导上传图片
```

#### 6\.1\.2 缓存策略细节

**热门卡密缓存**：

- 最近 1 小时内被查看的卡密结果，缓存到 Redis

- 缓存过期时间：1 小时

- 查看次数 \+ 1 时自动续期

**缓存 Key 设计**：

```python
def get_cache_key(card_id):
    """生成缓存Key"""
    return f"analysis:result:{card_id}"

# 缓存配置
CACHE_CONFIG = {
    'EXPIRE_TIME': 3600,  # 1小时
    'AUTO_RENEW': True,   # 访问时自动续期
    'MAX_CACHE_SIZE': 100000  # 最大缓存条目数
}
```

**冷数据存储**：

- 超过 1 小时未访问的数据，仅存在 MySQL 中

- 再次访问时自动预热到缓存

**性能指标**：

- 缓存命中率：≥ 80%

- 结果加载时间：
・缓存命中：\&lt; 100ms
・数据库查询：\&lt; 500ms
・首次分析：15\-20 秒

#### 6\.1\.3 缓存实现代码

```python
import redis
import json
from datetime import timedelta

class AnalysisCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.expire_time = 3600  # 1小时
    
    def get_result(self, card_id):
        """获取分析结果，优先从缓存读取"""
        cache_key = get_cache_key(card_id)
        
        # 尝试从缓存读取
        cached = self.redis.get(cache_key)
        if cached:
            # 自动续期
            self.redis.expire(cache_key, self.expire_time)
            return json.loads(cached), True
        
        # 缓存未命中，从数据库读取
        result = self._get_from_database(card_id)
        if result:
            # 写入缓存
            self.redis.setex(
                cache_key,
                self.expire_time,
                json.dumps(result, ensure_ascii=False)
            )
            return result, False
        
        return None, False
    
    def set_result(self, card_id, result):
        """新生成结果时写入缓存"""
        cache_key = get_cache_key(card_id)
        self.redis.setex(
            cache_key,
            self.expire_time,
            json.dumps(result, ensure_ascii=False)
        )
    
    def invalidate(self, card_id):
        """删除缓存（用户主动删除数据时）"""
        cache_key = get_cache_key(card_id)
        self.redis.delete(cache_key)
    
    def _get_from_database(self, card_id):
        """从数据库读取结果"""
        from models import AnalysisResult
        ar = AnalysisResult.objects.filter(
            card_id=card_id,
            is_deleted=False
        ).first()
        if ar:
            # 更新查看统计
            ar.view_count += 1
            ar.last_view_at = datetime.now()
            ar.save()
            return ar.result_json
        return None
```

### 6\.2 核心后端接口定义

#### 6\.2\.1 卡密验证接口

```Plain Text
POST /api/card/verify
Content-Type: application/json

Request:
{
  "card_id": "ABCD-1234-EFGH-5678"
}

Response（未激活）:
{
  "code": 0,
  "status": "not_activated",
  "message": "卡密验证成功，请上传图片",
  "data": {
    "card_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expire_at": "2027-05-01T12:00:00"
  }
}

Response（已激活）:
{
  "code": 0,
  "status": "activated",
  "message": "找到分析报告",
  "data": {
    "analysis_id": "xxxxxx",
    "created_at": "2026-05-01T12:00:00",
    "view_count": 3,
    "last_view_at": "2026-05-02T15:30:00"
  }
}

Response（已使用/过期）:
{
  "code": 4001,
  "status": "used",
  "message": "该卡密已被使用或已过期",
  "data": {
    "recommend_url": "/buy",
    "invite_url": "/invite"
  }
}
```

**接口实现代码**：

```python
@api.route('/api/card/verify', methods=['POST'])
def verify_card():
    data = request.get_json()
    card_id = data.get('card_id', '').strip().upper()
    
    # 格式校验
    if not re.match(r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$', card_id):
        return jsonify({
            'code': 4000,
            'message': '卡密格式错误'
        }), 400
    
    # 防暴力破解检查
    if is_rate_limited(request.remote_addr):
        return jsonify({
            'code': 4290,
            'message': '请求过于频繁，请稍后再试'
        }), 429
    
    # 查询卡密
    card = Card.objects.filter(card_id=card_id).first()
    
    if not card:
        record_failed_attempt(request.remote_addr)
        return jsonify({
            'code': 4004,
            'message': '卡密不存在'
        }), 404
    
    # 检查是否过期
    if card.expire_at < datetime.now():
        card.status = 'expired'
        card.save()
        return jsonify({
            'code': 4001,
            'status': 'expired',
            'message': '该卡密已过期',
            'data': {'recommend_url': '/buy'}
        })
    
    # 根据状态返回
    if card.status == 'not_activated':
        # 生成上传令牌
        card_token = generate_card_token(card_id)
        return jsonify({
            'code': 0,
            'status': 'not_activated',
            'message': '卡密验证成功，请上传图片',
            'data': {
                'card_token': card_token,
                'expire_at': card.expire_at.isoformat()
            }
        })
    
    elif card.status == 'activated':
        return jsonify({
            'code': 0,
            'status': 'activated',
            'message': '找到分析报告',
            'data': {
                'created_at': card.activated_at.isoformat(),
                'view_count': get_view_count(card_id),
                'last_view_at': get_last_view_at(card_id)
            }
        })
    
    else:
        return jsonify({
            'code': 4001,
            'status': card.status,
            'message': '该卡密已被使用',
            'data': {'recommend_url': '/buy'}
        })
```

#### 6\.2\.2 结果查询接口

```Plain Text
POST /api/analysis/get
Content-Type: application/json

Request:
{
  "card_id": "ABCD-1234-EFGH-5678"
}

Response:
{
  "code": 0,
  "data": {
    "summary": {
      "overall_score": 85,
      "personality": "你是一个理性且务实的人...",
      "career_tendency": "适合从事技术或管理工作"
    },
    "left_hand": {
      "life_line": {...},
      "heart_line": {...},
      "head_line": {...}
    },
    "right_hand": {
      "life_line": {...},
      "heart_line": {...},
      "head_line": {...}
    },
    "face": {
      "forehead": {...},
      "eyes": {...},
      "nose": {...},
      "mouth": {...}
    },
    "generated_at": "2026-05-01T12:00:00"
  },
  "meta": {
    "from_cache": true,
    "response_time": "85ms"
  }
}
```

#### 6\.2\.3 数据删除接口

```Plain Text
POST /api/privacy/delete
Content-Type: application/json

Request:
{
  "card_id": "ABCD-1234-EFGH-5678",
  "confirm": true
}

Response:
{
  "code": 0,
  "message": "数据已永久删除",
  "data": {
    "deleted_items": {
      "analysis_result": true,
      "cached_data": true,
      "images": 2
    }
  }
}
```

**数据删除实现**：

```python
@api.route('/api/privacy/delete', methods=['POST'])
def delete_privacy_data():
    data = request.get_json()
    card_id = data.get('card_id', '').strip().upper()
    confirm = data.get('confirm', False)
    
    if not confirm:
        return jsonify({
            'code': 4000,
            'message': '请确认删除操作'
        }), 400
    
    deleted_count = {
        'analysis_result': False,
        'cached_data': False,
        'images': 0
    }
    
    # 1. 删除分析结果
    ar = AnalysisResult.objects.filter(card_id=card_id).first()
    if ar:
        ar.is_deleted = True
        ar.deleted_at = datetime.now()
        ar.save()
        deleted_count['analysis_result'] = True
    
    # 2. 清除缓存
    cache = AnalysisCache()
    cache.invalidate(card_id)
    deleted_count['cached_data'] = True
    
    # 3. 删除关联图片
    images = ImageUpload.objects.filter(card_id=card_id, is_deleted=False)
    for img in images:
        if os.path.exists(img.file_path):
            os.remove(img.file_path)
        img.is_deleted = True
        img.deleted_at = datetime.now()
        img.save()
        deleted_count['images'] += 1
    
    # 4. 标记卡密为已使用
    card = Card.objects.filter(card_id=card_id).first()
    if card:
        card.status = 'used'
        card.save()
    
    # 5. 记录删除审计日志
    log_privacy_deletion(card_id, deleted_count)
    
    return jsonify({
        'code': 0,
        'message': '数据已永久删除，无法恢复',
        'data': {'deleted_items': deleted_count}
    })
```

### 6\.3 数据自动清理任务实现方案

#### 6\.3\.1 定时任务配置

**Celery 定时任务配置**：

```python
# celery_config.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'daily-privacy-cleanup': {
        'task': 'tasks.cleanup_privacy_data',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点执行
    },
    'hourly-cache-maintenance': {
        'task': 'tasks.maintain_cache',
        'schedule': crontab(minute=0),  # 每小时执行
    }
}
```

#### 6\.3\.2 完整清理任务实现

```python
# tasks.py
from celery import shared_task
from datetime import datetime, timedelta
import os

@shared_task
def cleanup_privacy_data():
    """每日隐私数据清理任务"""
    start_time = datetime.now()
    stats = {
        'images_deleted': 0,
        'analysis_deleted': 0,
        'expired_cards': 0,
        'logs_sanitized': 0
    }
    
    # 1. 删除24小时前的图片
    stats['images_deleted'] = cleanup_old_images(hours=24)
    
    # 2. 删除1年前的分析结果
    stats['analysis_deleted'] = cleanup_old_analysis(years=1)
    
    # 3. 处理过期卡密
    stats['expired_cards'] = cleanup_expired_cards()
    
    # 4. 清理日志
    stats['logs_sanitized'] = sanitize_system_logs()
    
    # 5. 记录统计
    duration = (datetime.now() - start_time).total_seconds()
    log_cleanup_completion(stats, duration)
    
    return stats

def cleanup_old_images(hours=24):
    """清理过期图片"""
    cutoff = datetime.now() - timedelta(hours=hours)
    deleted = 0
    
    images = ImageUpload.objects.filter(
        created_at__lt=cutoff,
        is_deleted=False
    )
    
    for img in images:
        try:
            if os.path.exists(img.file_path):
                os.remove(img.file_path)
            img.is_deleted = True
            img.deleted_at = datetime.now()
            img.save()
            deleted += 1
        except Exception as e:
            log_error(f"Failed to delete image {img.id}: {e}")
    
    return deleted

def cleanup_old_analysis(years=1):
    """清理过期分析结果"""
    cutoff = datetime.now() - timedelta(days=365 * years)
    deleted = 0
    
    results = AnalysisResult.objects.filter(
        created_at__lt=cutoff,
        is_deleted=False
    )
    
    for ar in results:
        ar.is_deleted = True
        ar.deleted_at = datetime.now()
        ar.save()
        # 同时清除缓存
        cache = AnalysisCache()
        cache.invalidate(ar.card_id)
        deleted += 1
    
    return deleted
```

### 6\.4 安全防护措施

#### 6\.4\.1 防暴力破解防护

```python
# rate_limit.py
import redis
from datetime import timedelta

class RateLimiter:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=1)
        self.max_attempts = 5
        self.window_seconds = 3600  # 1小时
    
    def is_limited(self, ip_address):
        """检查IP是否被限制"""
        key = f"rate_limit:card_verify:{ip_address}"
        attempts = self.redis.get(key)
        
        if attempts and int(attempts) >= self.max_attempts:
            return True
        return False
    
    def record_attempt(self, ip_address):
        """记录一次失败尝试"""
        key = f"rate_limit:card_verify:{ip_address}"
        self.redis.incr(key)
        self.redis.expire(key, self.window_seconds)
    
    def reset_attempts(self, ip_address):
        """验证成功时重置计数"""
        key = f"rate_limit:card_verify:{ip_address}"
        self.redis.delete(key)
```

#### 6\.4\.2 传输与存储安全

1. **HTTPS 全程加密**：全站强制 HTTPS，HSTS 配置

2. **数据库加密**：敏感字段使用 AES\-256 加密存储

3. **请求签名**：重要接口使用 API 签名验证

4. **SQL 注入防护**：ORM 参数化查询，输入过滤

5. **XSS 防护**：输出转义，CSP 安全策略

---

## 第 7 章 性能与监控

### 7\.1 性能指标

|指标|目标值|
|---|---|
|缓存命中率|≥ 80%|
|缓存响应时间|\&lt; 100ms|
|数据库响应时间|\&lt; 500ms|
|AI 分析耗时|15\-20 秒|
|系统可用性|≥ 99\.9%|

### 7\.2 监控告警

1. **缓存命中率监控**：低于 70% 触发告警

2. **接口响应时间监控**：超过 1 秒触发告警

3. **错误率监控**：超过 5% 触发告警

4. **清理任务监控**：任务失败触发告警

---

## 第 8 章 合规与风险控制

### 8\.1 隐私政策更新

在首页和结果页底部展示隐私声明：

> 🔒 隐私保护承诺
> 
> 1. **图片处理**：我们仅存储分析结果文本，原始图片上传后 24 小时自动永久删除，不留任何备份
> 
> 2. **身份匿名**：我们不收集任何个人身份信息，无需注册登录，不关联手机号、微信等账号
> 
> 3. **数据控制**：你可以随时永久删除你的所有数据，删除后无法恢复
> 
> 4. **数据加密**：所有数据加密存储，仅与你的卡密关联，无法追溯到个人
> 
> 5. **数据保留**：分析结果数据保留期限为 1 年，到期自动删除，你也可以随时主动删除
> 
> 6. **第三方共享**：我们绝不会将你的数据分享给任何第三方机构或个人
> 
> 

### 8\.2 数据安全合规说明

#### 8\.2\.1 用户匿名化合规

- **无账号体系**：符合《个人信息保护法》最小必要原则

- **去标识化处理**：所有数据仅与卡密关联，卡密本身不包含任何个人信息

- **不可追溯**：技术上确保无法通过卡密反推用户身份

- **数据隔离**：不同卡密数据物理隔离，无交叉关联可能

#### 8\.2\.2 数据生命周期合规

- **收集限制**：仅收集完成 AI 分析必需的图片数据

- **存储限制**：图片 24 小时删除，分析结果 1 年删除

- **用户控制权**：提供主动删除功能，用户拥有数据最终控制权

- **删除保障**：删除操作不可撤销，物理删除而非逻辑删除

#### 8\.2\.3 合规审计机制

1. **定期审计**：每季度进行数据安全审计

2. **日志留存**：所有数据操作日志留存 6 个月

3. **违规告警**：异常数据访问自动告警

4. **合规报告**：每年发布数据合规报告

### 8\.3 风险控制措施

|风险点|控制措施|
|---|---|
|卡密被盗用|分享卡片自动脱敏，限制查看设备数|
|暴力破解|IP 限流 \+ 16 位高复杂度卡密|
|数据泄露|加密存储 \+ 最小权限访问控制|
|合规风险|定期合规审计 \+ 隐私政策更新|
|服务滥用|卡密使用频次限制 \+ 异常行为检测|

---

## 第 9 章 版本历史

|版本|发布日期|主要更新|
|---|---|---|
|v4\.0|2026\-05\-01|卡密系统优化、多级缓存升级、隐私保护增强、用户体验优化|
|v3\.9|2026\-04\-15|基础卡密功能、基础缓存机制|
|v3\.8|2026\-04\-01|AI 分析引擎优化|
|v3\.7|2026\-03\-15|H5 界面重构|

---

## 附录 A：接口完整文档

详见《API 接口文档 \[v4\.0\.md\]\(v4\.0\.md\)》

## 附录 B：数据库设计文档

详见《数据库设计说明书 \[v4\.0\.md\]\(v4\.0\.md\)》

## 附录 C：部署运维手册

详见《部署运维手册 \[v4\.0\.md\]\(v4\.0\.md\)》

> （注：文档部分内容可能由 AI 生成）
