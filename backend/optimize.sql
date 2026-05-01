-- 1. 优化 cards 表
-- 加速管理后台按状态筛选卡密，以及按创建/激活时间排序
CREATE INDEX idx_cards_status_created ON ai_hand_analysis.cards (status, created_at DESC);
CREATE INDEX idx_cards_status_activated ON ai_hand_analysis.cards (status, activated_at DESC);

-- 2. 优化 interpretation_caches 表
-- 目前代码中频繁使用 card_id 和 mode 进行复合查询，虽然有 UniqueConstraint，
-- 但增加一个显式的复合索引可以进一步优化某些数据库引擎的查询计划
CREATE INDEX idx_interpretation_card_mode ON ai_hand_analysis.interpretation_caches (card_id, mode, is_deleted);

-- 3. 优化 analysis_results 表
-- 加速管理后台的互动数据列表展示（按最近查看时间排序）
CREATE INDEX idx_analysis_results_view_stats ON ai_hand_analysis.analysis_results (is_deleted, last_view_at DESC);
CREATE INDEX idx_analysis_results_created ON ai_hand_analysis.analysis_results (is_deleted, created_at DESC);

-- 4. 统计性能优化（可选）
-- 如果后续数据量达到百万级，这些索引将显著提升管理后台“概览看板”的加载速度
CREATE INDEX idx_cards_status ON ai_hand_analysis.cards (status);