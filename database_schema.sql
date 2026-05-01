CREATE DATABASE `ai_hand_analysis` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */

CREATE TABLE ai_hand_analysis.`cards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_id` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('NOT_ACTIVATED','ACTIVATED','USED','EXPIRED') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `activated_at` datetime DEFAULT NULL,
  `expire_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_cards_card_id` (`card_id`),
  KEY `ix_cards_id` (`id`),
  KEY `idx_cards_status` (`status`),
  KEY `idx_cards_status_created` (`status`,`created_at` DESC),
  KEY `idx_cards_status_activated` (`status`,`activated_at` DESC)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE ai_hand_analysis.`analysis_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_id` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `result_json` json NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `view_count` int DEFAULT NULL,
  `last_view_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_analysis_results_card_id` (`card_id`),
  KEY `ix_analysis_results_id` (`id`),
  KEY `idx_analysis_results_view_stats` (`is_deleted`,`last_view_at` DESC),
  KEY `idx_analysis_results_created` (`is_deleted`,`created_at` DESC)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE ai_hand_analysis.`interpretation_caches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `card_id` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `mode` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `result_json` json NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `is_deleted` tinyint(1) DEFAULT '0',
  `deleted_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_card_interpretation_mode` (`card_id`,`mode`),
  KEY `ix_interpretation_caches_card_id` (`card_id`),
  KEY `ix_interpretation_caches_mode` (`mode`),
  KEY `ix_interpretation_caches_id` (`id`),
  KEY `idx_interpretation_card_mode` (`card_id`,`mode`,`is_deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
