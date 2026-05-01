# AI手相面相分析H5服务 \- UI/UX设计规范 v4\.0

**版本号**：v4\.0
**更新日期**：2026\-05\-01
**适用范围**：H5 移动端全平台（微信、Safari、安卓浏览器、PC 端）

---

## 目录

1. \[卡密相关页面 UI 设计更新\]\(\#1\-卡密相关页面ui设计更新\)

2. \[隐私保护 UI 元素新增\]\(\#2\-隐私保护ui元素新增\)

3. \[页面流程更新\]\(\#3\-页面流程更新\)

4. \[微交互与动效更新\]\(\#4\-微交互与动效更新\)

5. \[响应式与兼容性更新\]\(\#5\-响应式与兼容性更新\)

6. \[设计系统版本更新\]\(\#6\-设计系统版本更新\)

7. \[CSS 代码示例\]\(\#7\-css代码示例\)

8. \[附录\]\(\#8\-附录\)

---

## 1\. 卡密相关页面 UI 设计更新

### 1\.1 卡密输入页全新设计

#### 页面布局

**顶部区域**

- 返回按钮：24px × 24px，距离左边缘 16px，距离顶部 44px

- 标题：\&\#34;输入你的分析卡密\&\#34;，字体大小 20px，字重 600，居中对齐，距离顶部 44px

**中间区域**

- 大图标：🔐 金色锁形图标，尺寸 80px × 80px，带发光效果

    - 图标颜色：\#F59E0B（金色）

    - 发光效果：box\-shadow: 0 0 30px rgba \(245, 158, 11, 0\.4\)

    - 距离顶部：80px

- 提示文案：\&\#34;输入 16 位卡密，即可查看你的专属分析报告\&\#34;

    - 字体大小：16px

    - 颜色：\#6B7280

    - 对齐方式：居中

    - 距离图标下方：24px

- 卡密输入框：4 组 ×4 位输入框设计

    - 每组之间用 \&\#34;\-\&\#34; 分隔，分隔符颜色 \#9CA3AF，字号 24px

    - 输入框大小：56px × 56px

    - 输入框间距：每组之间 8px，组内 4px

    - 边框：2px solid \#E5E7EB，圆角 12px

    - 字体：等宽字体（\&\#39;SF Mono\&\#39;, \&\#39;Monaco\&\#39;, monospace），字号 24px，字重 700

    - 输入完成自动跳格

    - 聚焦时边框渐变发光：border\-image: linear\-gradient \(135deg, \#F59E0B, \#EF4444\) 1

- 快捷功能区：

    - \&\#34;粘贴卡密\&\#34; 按钮：检测到剪贴板有 16 位字符时自动显示

        - 背景：\#10B981，文字白色，字号 14px

        - 内边距：8px 16px，圆角 8px

        - 距离输入框下方：16px

    - \&\#34;最近使用\&\#34;：LocalStorage 存储的历史卡密，点击快速填入

        - 标签文字：\&\#34;最近使用\&\#34;，字号 14px，颜色 \#6B7280

        - 历史卡密标签：背景 \#F3F4F6，字号 14px，内边距 6px 12px，圆角 6px

        - 最多显示 3 条历史记录

**底部区域**

- 主按钮：\&\#34;验证卡密\&\#34;

    - 渐变背景：linear\-gradient \(135deg, \#F59E0B 0%, \#EF4444 100%\)

    - 文字颜色：白色，字号 18px，字重 600

    - 尺寸：100% 宽度，高度 56px，圆角 16px

    - 距离底部：40px

- 辅助链接：

    - \&\#34;没有卡密？立即购买\&\#34; \| \&\#34;邀请好友免费得\&\#34;

    - 字号 14px，颜色 \#3B82F6

    - 链接之间用 \&\#34;\|\&\#34; 分隔，颜色 \#9CA3AF

    - 距离主按钮下方：16px

- 隐私提示小字：

    - \&\#34;🔒 你的数据全程加密保护\&\#34;

    - 字号 12px，颜色 \#9CA3AF

    - 距离辅助链接下方：24px

#### 状态反馈设计

**✅ 验证成功 \- 未激活卡密**

- 弹窗动画：绿色对勾圆圈缩放动画（300ms）

- 弹窗尺寸：320px 宽度，自适应高度

- 背景：白色，圆角 20px，阴影 0 20px 60px rgba \(0,0,0,0\.15\)

- 文案：

    > 🎉 卡密验证成功！
    > 
    > 这是一张全新的分析卡
    > 接下来请上传你的手相 / 面相照片
    > 
    > 

- 按钮：\&\#34;开始上传照片\&\#34;

    - 背景：\#10B981，文字白色

    - 高度 48px，圆角 12px，100% 宽度

**✅ 验证成功 \- 已激活卡密（有缓存）**

- 弹窗动画：金色文档图标飞入动画（400ms）

- 文案：

    > 📄 找到你的分析报告！
    > 
    > 生成时间：2026\-05\-01 14:30
    > 已查看 3 次
    > 
    > 

- 按钮：\&\#34;立即查看报告\&\#34;

    - 渐变背景：linear\-gradient \(135deg, \#F59E0B, \#D97706\)

    - 文字白色

**❌ 验证失败**

- 弹窗动画：红色叉号抖动动画（300ms）

- 文案：

    > ❌ 卡密无效
    > 
    > 该卡密已被使用、已过期或不存在
    > 
    > 

- 按钮：\&\#34;重新输入\&\#34;（灰色背景）\| \&\#34;购买新卡密\&\#34;（红色背景）

---

### 1\.2 结果页卡密展示区更新

#### 顶部卡密提醒栏（固定在结果页顶部）

- 背景：渐变金色条 linear\-gradient \(90deg, rgba \(245, 158, 11, 0\.1\), rgba \(245, 158, 11, 0\.05\)\)

- 毛玻璃效果：backdrop\-filter: blur \(10px\)

- 高度：64px

- 内边距：水平 16px

- 左侧图标：💡，尺寸 24px × 24px

- 中间文案：

    > 请记住你的卡密
    > `ABCD\-1234\-EFGH\-5678`
    > 下次输入卡密即可直接查看，无需重新上传
    > 
    > 

    - 主标题：字号 14px，字重 600，颜色 \#92400E

    - 卡密：字号 16px，字重 700，颜色 \#B45309，字体等宽

    - 副标题：字号 12px，颜色 \#B45309

- 右侧按钮：

    - \&\#34;复制\&\#34; 按钮：背景 \#F59E0B，文字白色，字号 12px，内边距 6px 12px，圆角 6px

    - \&\#34;分享\&\#34; 按钮：背景白色，边框 1px solid \#F59E0B，文字 \#F59E0B，字号 12px，内边距 6px 12px，圆角 6px

    - 按钮间距：8px

#### 隐私保护操作区

- 在个人中心或设置页增加：

    - 🔒 隐私中心入口

        - 图标尺寸 20px，文字 \&\#34;隐私中心\&\#34;，字号 16px

        - 右侧箭头指示器

        - 行高 56px，底部边框 1px solid \#E5E7EB

    - 按钮：\&\#34;永久删除我的数据\&\#34;，红色警告样式

        - 背景：\#FEE2E2

        - 文字颜色：\#DC2626，字号 16px，字重 600

        - 高度：48px，圆角 12px

        - 100% 宽度，距离顶部 24px

- 二次确认弹窗：

    > ⚠️ 确认删除所有数据？
    > 
    > 删除后将无法恢复，卡密也将永久失效
    > 此操作不可撤销
    > 
    > 

    - 按钮：\&\#34;确认删除\&\#34;（红色背景 \#DC2626，白色文字）\| \&\#34;取消\&\#34;（灰色背景）

---

## 2\. 隐私保护 UI 元素新增

### 2\.1 全局隐私标识

**所有页面底部统一添加**

- 小字文案：\&\#34;🔒 隐私保护承诺：图片 24 小时自动删除・不收集个人信息・支持随时删除\&\#34;

- 字号：12px

- 颜色：\#9CA3AF

- 对齐方式：居中

- 内边距：上下 16px

- 可点击跳转到隐私政策详情页

- 点击效果：文字颜色变为 \#6B7280，背景轻微高亮

---

### 2\.2 上传页隐私提示

**在上传页面增加醒目提示**

- 卡片样式：

    - 背景：rgba \(16, 185, 129, 0\.05\)

    - 边框：2px solid \#10B981

    - 圆角：16px

    - 内边距：20px

    - 距离上传按钮上方：24px

- 图标：🛡️，尺寸 32px × 32px，居中

- 标题：\&\#34;你的隐私，我们全力保护\&\#34;

    - 字号：18px，字重 600

    - 颜色：\#065F46

    - 对齐：居中

    - 距离图标下方：12px

- 内容列表：

    - ✅ 原始图片 24 小时后自动永久删除

    - ✅ 不需要注册登录，不收集任何身份信息

    - ✅ 所有数据仅与你的卡密绑定

    - ✅ 支持随时一键永久删除所有数据

    - 列表项间距：8px

    - 字号：14px

    - 颜色：\#047857

---

### 2\.3 分享卡片隐私优化

**分享卡片卡密显示规则**

- 默认显示：`ABCD\-\*\*\*\*\-\*\*\*\*\-5678`（中间 8 位隐藏）

    - 隐藏字符使用 \&\#34;\*\&\#34;，颜色 \#9CA3AF

- 用户可选择：\&\#34;完全隐藏卡密\&\#34; 或 \&\#34;显示完整卡密\&\#34;

    - 开关控件在分享页顶部

    - UISwitch 样式，开启状态绿色 \#10B981

- 提示文案：\&\#34;建议隐藏卡密，防止他人盗用\&\#34;

    - 字号：12px

    - 颜色：\#F59E0B

    - 背景：rgba \(245, 158, 11, 0\.1\)

    - 内边距：8px 12px，圆角 8px

    - 距离开关下方：8px

---

## 3\. 页面流程更新

### 3\.1 完整用户旅程更新

**旧流程**：首页 → 上传页 → 卡密页 → 加载页 → 结果页

**新流程（v4\.0）**：

```mermaid
flowchart TD
    A[首页] --> B[卡密输入页]
    B --> C{验证卡密状态}
    C -->|未激活| D[上传页]
    D --> E[加载页]
    E --> F[结果页<br/>显示卡密+删除按钮]
    C -->|已激活| G[直接跳转到结果页<br/>从缓存读取]
    G --> H[退出后再次进入]
    H --> B
    F --> H
    
    style A fill:#E0E7FF,stroke:#6366F1
    style B fill:#DBEAFE,stroke:#3B82F6
    style C fill:#D1FAE5,stroke:#10B981
    style D fill:#FEF3C7,stroke:#F59E0B
    style E fill:#FEE2E2,stroke:#EF4444
    style F fill:#E0E7FF,stroke:#6366F1
    style G fill:#F3E8FF,stroke:#8B5CF6```

---

### 3\.2 新增页面

#### 1\. 卡密输入页（独立页面，原在上传页内）

- 独立路由：`/card\-input`

- 页面标题：\&\#34;卡密验证\&\#34;

- 支持直接分享链接进入

#### 2\. 隐私中心页

- 独立路由：`/privacy\-center`

- 详细说明隐私保护措施

- 删除数据按钮

- 隐私政策全文链接

- 常见问题解答

#### 3\. 卡密购买页

- 独立路由：`/buy\-card`

- 展示不同套餐：

    - 单次分析卡：¥9\.9

    - 3 次卡套餐：¥24\.9（省 ¥5）

    - 10 次卡套餐：¥69\.9（省 ¥30）

- 支付方式选择：微信支付 / 支付宝

- 购买成功后自动生成卡密

---

## 4\. 微交互与动效更新

### 4\.1 卡密输入动效

- 每个数字输入时：从上方弹入，轻微缩放动画

    ```css
    @keyframes keyIn {
      0% { transform: translateY(-10px) scale(0.8); opacity: 0; }
      100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    .digit-enter { animation: keyIn 150ms ease-out; }
    ```

- 输入完成一组后：自动跳到下一组，焦点框平滑移动

    ```css
    .focus-ring {
      transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    ```

- 粘贴时：4 组同时填入，依次亮起

    - 延迟：每组 50ms 间隔

    - 总时长：200ms

- 验证中：按钮显示旋转加载动画，输入框轻微呼吸效果

    ```css
    @keyframes breathe {
      0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
      50% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
    }
    .verifying { animation: breathe 1.5s ease-in-out infinite; }
    ```

---

### 4\.2 数据删除动效

- 点击删除后：碎纸机动画，数据卡片被撕碎消失

    ```css
    @keyframes shred {
      0% { transform: translateY(0) rotate(0deg); opacity: 1; }
      100% { transform: translateY(100px) rotate(5deg); opacity: 0; }
    }
    .shredding {
      animation: shred 500ms ease-in forwards;
      clip-path: inset(0 0 0 0);
    }
    ```

- 完成后：绿色对勾 \+ \&\#34;数据已永久删除\&\#34; 提示

    - 对勾动画：缩放弹入效果，300ms

    - 提示文字渐入，200ms 延迟

- 自动跳转到首页，卡密已失效

    - 跳转延迟：1500ms

    - 转场动画：淡入淡出，300ms

---

### 4\.3 缓存加载动效

- 已激活卡密加载时：

    - 不显示四阶段分析动画（因为不需要重新分析）

    - 改为：文档图标从云端下载到本地的动画

    - 文案：\&\#34;正在加载你的专属报告\.\.\.\&\#34;

    - 耗时：1\-2 秒（远快于首次分析）

```css
@keyframes cloudDownload {
  0% { transform: translateY(-20px); opacity: 0; }
  50% { transform: translateY(5px); }
  100% { transform: translateY(0); opacity: 1; }
}
.cloud-icon { animation: cloudDownload 800ms ease-out; }
```

---

## 5\. 响应式与兼容性更新

### 5\.1 卡密输入框适配

|设备类型|屏幕宽度|输入框尺寸|间距调整|
|---|---|---|---|
|iPhone SE（小屏）|\&lt; 375px|48px × 48px|组间距 6px，组内 3px|
|标准手机|375px \- 430px|56px × 56px|组间距 8px，组内 4px|
|大屏手机|430px \- 768px|56px × 56px|最大宽度 400px，居中|
|平板 / PC|\&gt; 768px|56px × 56px|最大宽度 480px，居中|

**断点设置**：

- sm: 375px

- md: 768px

- lg: 1024px

---

### 5\.2 粘贴功能兼容性

|环境|支持方式|实现细节|
|---|---|---|
|微信环境|支持长按粘贴|监听 input 的 paste 事件|
|iOS Safari|支持系统粘贴板|使用 navigator\.clipboard\.readText \(\)|
|安卓各浏览器|兼容处理|降级到长按粘贴方案|
|PC 端|支持 Ctrl\+V 粘贴|监听 keydown 事件检测 Ctrl\+V|

**降级策略**：

- 如剪贴板 API 不可用，隐藏 \&\#34;粘贴卡密\&\#34; 按钮

- 保留手动输入功能

- 提示用户 \&\#34;请手动输入 16 位卡密\&\#34;

---

## 6\. 设计系统版本更新

### 6\.1 颜色系统

**新增颜色**：

- 隐私绿：`\#10B981` \- 用于隐私标识、成功状态

- 隐私绿浅：`rgba\(16, 185, 129, 0\.05\)` \- 用于隐私提示背景

- 隐私绿深：`\#065F46` \- 用于隐私提示文字

**完整色板**：

```css
:root {
  /* 主色调 */
  --primary-gold: #F59E0B;
  --primary-red: #EF4444;
  --primary-gradient: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
  
  /* 新增：隐私绿 */
  --privacy-green: #10B981;
  --privacy-green-light: rgba(16, 185, 129, 0.05);
  --privacy-green-dark: #065F46;
  
  /* 中性色 */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-400: #9CA3AF;
  --gray-500: #6B7280;
  --gray-600: #4B5563;
  --gray-700: #374151;
  --gray-800: #1F2937;
  --gray-900: #111827;
}
```

---

### 6\.2 组件库

**新增组件**：

1. **卡密输入框组件** \(`\&lt;card\-input\&gt;`\)

    - Props: length=16, groups=4, digitsPerGroup=4

    - Events: @complete, @change, @paste

    - Methods: focus\(\), clear\(\), getValue\(\)

2. **隐私提示卡片组件** \(`\&lt;privacy\-card\&gt;`\)

    - Props: type=\&\#34;info\&\#34;, title, items

    - Slots: default, icon

3. **状态弹窗组件** \(`\&lt;status\-modal\&gt;`\)

    - Props: type=\&\#34;success\|error\|info\&\#34;, title, message, buttons

    - 支持自定义图标和动画

---

### 6\.3 图标库

**新增图标**：

- 🔐 锁形图标（金色，带发光效果）

- 📄 文档图标（金色）

- 🛡️ 盾牌图标（绿色）

- ✂️ 碎纸机图标（红色）

- ☁️ 云端下载图标

- 💡 提示灯泡图标

**图标规范**：

- 尺寸：24px / 32px / 48px / 80px

- 线条粗细：2px

- 圆角：2px

- 颜色：使用设计系统色值

---

### 6\.4 动效库

**新增动画**：

- `keyIn` \- 数字输入弹入

- `breathe` \- 呼吸效果

- `shred` \- 碎纸机效果

- `cloudDownload` \- 云端下载

- `successCheck` \- 成功对勾缩放

- `errorShake` \- 错误抖动

**动画时长规范**：

- 快速反馈：150ms（按键、点击）

- 标准转场：300ms（页面切换、弹窗）

- 复杂动画：400\-800ms（特殊效果）

- 循环动画：1500ms（加载、呼吸）

---

## 7\. CSS 代码示例

### 7\.1 卡密输入框完整样式

```css
.card-input-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.card-input-group {
  display: flex;
  gap: 4px;
}

.card-input-group:not(:last-child)::after {
  content: '-';
  display: flex;
  align-items: center;
  color: #9CA3AF;
  font-size: 24px;
  font-weight: 700;
  margin-left: 4px;
}

.card-input-digit {
  width: 56px;
  height: 56px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  text-align: center;
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 24px;
  font-weight: 700;
  outline: none;
  transition: all 200ms ease;
}

.card-input-digit:focus {
  border-color: transparent;
  border-image: linear-gradient(135deg, #F59E0B, #EF4444) 1;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.1);
}

.card-input-digit.filled {
  animation: keyIn 150ms ease-out;
}

/* 响应式适配 */
@media (max-width: 374px) {
  .card-input-digit {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }
}
```

---

### 7\.2 隐私提示卡片样式

```css
.privacy-card {
  background: rgba(16, 185, 129, 0.05);
  border: 2px solid #10B981;
  border-radius: 16px;
  padding: 20px;
}

.privacy-card-icon {
  text-align: center;
  font-size: 32px;
  margin-bottom: 12px;
}

.privacy-card-title {
  font-size: 18px;
  font-weight: 600;
  color: #065F46;
  text-align: center;
  margin-bottom: 16px;
}

.privacy-card-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.privacy-card-item {
  font-size: 14px;
  color: #047857;
  padding: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.privacy-card-item::before {
  content: '✅';
}
```

---

### 7\.3 验证按钮渐变样式

```css
.btn-primary {
  width: 100%;
  height: 56px;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
  cursor: pointer;
  transition: all 200ms ease;
  position: relative;
  overflow: hidden;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(245, 158, 11, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary.loading {
  pointer-events: none;
}

.btn-primary.loading::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  margin: -10px 0 0 -10px;
  border: 2px solid transparent;
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## 8\. 附录

### 8\.1 版本变更记录

|版本|日期|更新内容|
|---|---|---|
|v4\.0|2026\-05\-01|1\. 新增独立卡密输入页<br>2\. 新增隐私保护 UI 元素<br>3\. 更新用户旅程流程<br>4\. 新增微交互与动效<br>5\. 新增隐私绿色系<br>6\. 新增卡密输入框等组件|
|v3\.9|2026\-04\-15|基础版本功能完善|

### 8\.2 开发检查清单

* [ ] 卡密输入框 4×4 布局，自动跳格

* [ ] 剪贴板粘贴功能检测与自动填充

* [ ] 三种验证状态弹窗与动画

* [ ] 结果页顶部卡密提醒栏

* [ ] 数据删除二次确认与碎纸机动画

* [ ] 全局底部隐私标识

* [ ] 上传页隐私提示卡片

* [ ] 分享卡片卡密隐藏功能

* [ ] 新用户旅程流程实现

* [ ] 响应式适配各屏幕尺寸

* [ ] CSS 变量与设计系统色值统一

* [ ] 所有动效时长与缓动函数正确

---

**文档结束**

*本设计规范版本 v4\.0，所有开发请严格按照此规范执行，如有疑问请及时沟通*

> （注：文档部分内容可能由 AI 生成）
