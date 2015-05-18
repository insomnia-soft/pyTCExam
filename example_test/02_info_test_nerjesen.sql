-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: tcexam
-- ------------------------------------------------------
-- Server version	5.6.23-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tce_answers`
--

DROP TABLE IF EXISTS `tce_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_answers` (
  `answer_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `answer_question_id` bigint(20) unsigned NOT NULL,
  `answer_description` text COLLATE utf8_unicode_ci NOT NULL,
  `answer_explanation` text COLLATE utf8_unicode_ci,
  `answer_isright` tinyint(1) NOT NULL DEFAULT '0',
  `answer_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `answer_position` bigint(20) unsigned DEFAULT NULL,
  `answer_keyboard_key` smallint(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `p_answer_question_id` (`answer_question_id`),
  CONSTRAINT `tce_answers_ibfk_1` FOREIGN KEY (`answer_question_id`) REFERENCES `tce_questions` (`question_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_answers`
--

LOCK TABLES `tce_answers` WRITE;
/*!40000 ALTER TABLE `tce_answers` DISABLE KEYS */;
INSERT INTO `tce_answers` VALUES (1,1,'2',NULL,0,1,NULL,NULL),(2,1,'3',NULL,0,1,NULL,NULL),(3,1,'4',NULL,0,1,NULL,NULL),(4,1,'5',NULL,1,1,NULL,NULL),(5,2,'JPG',NULL,0,1,NULL,NULL),(6,2,'TIFF',NULL,0,1,NULL,NULL),(7,2,'BMP',NULL,0,1,NULL,NULL),(8,2,'GIF',NULL,1,1,NULL,NULL),(9,3,'=CIRCLE(B2;0)',NULL,0,1,NULL,NULL),(10,3,'=ROUND(B2;1)',NULL,0,1,NULL,NULL),(11,3,'=CIRCLE(B2;1)',NULL,0,1,NULL,NULL),(12,3,'=ROUND(B2;0)',NULL,1,1,NULL,NULL),(13,4,'staza',NULL,1,1,NULL,NULL),(14,4,'sektor',NULL,1,1,NULL,NULL),(15,4,'spirala',NULL,0,1,NULL,NULL),(16,4,'cilindar',NULL,1,1,NULL,NULL),(17,5,'200 000 B',NULL,0,1,1,NULL),(18,5,'2 047 KB',NULL,0,1,2,NULL),(19,5,'2 MB',NULL,0,1,3,NULL),(20,5,'0,2 GB',NULL,0,1,4,NULL),(21,6,'carnet',NULL,1,1,NULL,NULL);
/*!40000 ALTER TABLE `tce_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_modules`
--

DROP TABLE IF EXISTS `tce_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_modules` (
  `module_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `module_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `module_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `module_user_id` bigint(20) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`module_id`),
  UNIQUE KEY `ak_module_name` (`module_name`),
  KEY `p_module_user_id` (`module_user_id`),
  CONSTRAINT `tce_modules_ibfk_1` FOREIGN KEY (`module_user_id`) REFERENCES `tce_users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_modules`
--

LOCK TABLES `tce_modules` WRITE;
/*!40000 ALTER TABLE `tce_modules` DISABLE KEYS */;
INSERT INTO `tce_modules` VALUES (1,'default',1,1),(2,'modul 01',1,2);
/*!40000 ALTER TABLE `tce_modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_questions`
--

DROP TABLE IF EXISTS `tce_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_questions` (
  `question_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `question_subject_id` bigint(20) unsigned NOT NULL,
  `question_description` text COLLATE utf8_unicode_ci NOT NULL,
  `question_explanation` text COLLATE utf8_unicode_ci,
  `question_type` smallint(3) unsigned NOT NULL DEFAULT '1',
  `question_difficulty` smallint(6) NOT NULL DEFAULT '1',
  `question_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `question_position` bigint(20) unsigned DEFAULT NULL,
  `question_timer` smallint(10) DEFAULT NULL,
  `question_fullscreen` tinyint(1) NOT NULL DEFAULT '0',
  `question_inline_answers` tinyint(1) NOT NULL DEFAULT '0',
  `question_auto_next` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`question_id`),
  KEY `p_question_subject_id` (`question_subject_id`),
  CONSTRAINT `tce_questions_ibfk_1` FOREIGN KEY (`question_subject_id`) REFERENCES `tce_subjects` (`subject_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_questions`
--

LOCK TABLES `tce_questions` WRITE;
/*!40000 ALTER TABLE `tce_questions` DISABLE KEYS */;
INSERT INTO `tce_questions` VALUES (1,1,'Koji je dekadski zapis binarnog broja 101?',NULL,1,1,1,NULL,0,0,0,0),(2,1,'Koji od navedenih slikovnih formata omogućuje spremanje jednostavnih animacija?',NULL,1,1,1,NULL,0,0,0,0),(3,1,'U programu za proračunske tablice [i]MS Excel[/i] na adresi [b]B2[/b] upisana je vrijednost [b]2,8[/b].\r\nKako glasi formula kojom se ta vrijednost zaokružuje na najbliži cijeli broj?',NULL,1,1,1,NULL,0,0,0,0),(4,1,'Koji od navedenih pojmova [b]je[/b] izravno povezan s tvrdim diskom?',NULL,2,1,1,NULL,0,0,0,0),(5,1,'U kojem su nizu količine memorije poredane od najmanje prema najvećoj?',NULL,4,1,1,NULL,0,0,0,0),(6,1,'Napišite kraticu za Hrvatsku akademsku i istraživačku mrežu.',NULL,3,1,1,NULL,0,0,0,0);
/*!40000 ALTER TABLE `tce_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_sessions`
--

DROP TABLE IF EXISTS `tce_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_sessions` (
  `cpsession_id` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `cpsession_expiry` datetime NOT NULL,
  `cpsession_data` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cpsession_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_sessions`
--

LOCK TABLES `tce_sessions` WRITE;
/*!40000 ALTER TABLE `tce_sessions` DISABLE KEYS */;
INSERT INTO `tce_sessions` VALUES ('652b7715ca8fa33fad3508702cc531c0','2015-04-06 04:13:24','session_hash|s:32:\"d0bdafb6b2c2d2c873f0b3629a230f79\";session_user_id|s:1:\"3\";session_user_name|s:7:\"johndoe\";session_user_ip|s:39:\"0000:0000:0000:0000:0000:ffff:7f00:0001\";session_user_level|s:1:\"1\";session_user_firstname|s:0:\"\";session_user_lastname|s:0:\"\";session_test_login|s:0:\"\";session_last_visit|i:1428281577;logout|b:1;'),('671ca3cfd587c908fb0b68d7729cb0c1','2015-04-06 04:14:56','session_hash|s:32:\"8a890aa6f6b34cc6348a697de8c8753a\";session_user_id|s:1:\"2\";session_user_name|s:5:\"admin\";session_user_ip|s:39:\"0000:0000:0000:0000:0000:ffff:7f00:0001\";session_user_level|s:2:\"10\";session_user_firstname|s:0:\"\";session_user_lastname|s:0:\"\";session_test_login|s:0:\"\";session_last_visit|i:1428281574;logout|b:1;');
/*!40000 ALTER TABLE `tce_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_sslcerts`
--

DROP TABLE IF EXISTS `tce_sslcerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_sslcerts` (
  `ssl_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ssl_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ssl_hash` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `ssl_end_date` datetime NOT NULL,
  `ssl_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `ssl_user_id` bigint(20) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`ssl_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_sslcerts`
--

LOCK TABLES `tce_sslcerts` WRITE;
/*!40000 ALTER TABLE `tce_sslcerts` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_sslcerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_subjects`
--

DROP TABLE IF EXISTS `tce_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_subjects` (
  `subject_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `subject_module_id` bigint(20) unsigned NOT NULL DEFAULT '1',
  `subject_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `subject_description` text COLLATE utf8_unicode_ci,
  `subject_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `subject_user_id` bigint(20) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`subject_id`),
  UNIQUE KEY `ak_subject_name` (`subject_module_id`,`subject_name`),
  KEY `p_subject_user_id` (`subject_user_id`),
  CONSTRAINT `tce_subjects_ibfk_1` FOREIGN KEY (`subject_user_id`) REFERENCES `tce_users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `tce_subjects_ibfk_2` FOREIGN KEY (`subject_module_id`) REFERENCES `tce_modules` (`module_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_subjects`
--

LOCK TABLES `tce_subjects` WRITE;
/*!40000 ALTER TABLE `tce_subjects` DISABLE KEYS */;
INSERT INTO `tce_subjects` VALUES (1,2,'topic 01','Topic example for TCExam guide.',1,2);
/*!40000 ALTER TABLE `tce_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_test_subject_set`
--

DROP TABLE IF EXISTS `tce_test_subject_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_test_subject_set` (
  `tsubset_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tsubset_test_id` bigint(20) unsigned NOT NULL,
  `tsubset_type` smallint(6) NOT NULL DEFAULT '1',
  `tsubset_difficulty` smallint(6) NOT NULL DEFAULT '1',
  `tsubset_quantity` smallint(6) NOT NULL DEFAULT '1',
  `tsubset_answers` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`tsubset_id`),
  KEY `p_tsubset_test_id` (`tsubset_test_id`),
  CONSTRAINT `tce_test_subject_set_ibfk_1` FOREIGN KEY (`tsubset_test_id`) REFERENCES `tce_tests` (`test_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_test_subject_set`
--

LOCK TABLES `tce_test_subject_set` WRITE;
/*!40000 ALTER TABLE `tce_test_subject_set` DISABLE KEYS */;
INSERT INTO `tce_test_subject_set` VALUES (1,1,0,1,6,4);
/*!40000 ALTER TABLE `tce_test_subject_set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_test_subjects`
--

DROP TABLE IF EXISTS `tce_test_subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_test_subjects` (
  `subjset_tsubset_id` bigint(20) unsigned NOT NULL,
  `subjset_subject_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`subjset_tsubset_id`,`subjset_subject_id`),
  KEY `p_subjset_subject_id` (`subjset_subject_id`),
  KEY `p_subjset_tsubset_id` (`subjset_tsubset_id`),
  CONSTRAINT `tce_test_subjects_ibfk_1` FOREIGN KEY (`subjset_subject_id`) REFERENCES `tce_subjects` (`subject_id`) ON UPDATE NO ACTION,
  CONSTRAINT `tce_test_subjects_ibfk_2` FOREIGN KEY (`subjset_tsubset_id`) REFERENCES `tce_test_subject_set` (`tsubset_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_test_subjects`
--

LOCK TABLES `tce_test_subjects` WRITE;
/*!40000 ALTER TABLE `tce_test_subjects` DISABLE KEYS */;
INSERT INTO `tce_test_subjects` VALUES (1,1);
/*!40000 ALTER TABLE `tce_test_subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_testgroups`
--

DROP TABLE IF EXISTS `tce_testgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_testgroups` (
  `tstgrp_test_id` bigint(20) unsigned NOT NULL,
  `tstgrp_group_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`tstgrp_test_id`,`tstgrp_group_id`),
  KEY `p_tstgrp_test_id` (`tstgrp_test_id`),
  KEY `p_tstgrp_group_id` (`tstgrp_group_id`),
  CONSTRAINT `tce_testgroups_ibfk_1` FOREIGN KEY (`tstgrp_test_id`) REFERENCES `tce_tests` (`test_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `tce_testgroups_ibfk_2` FOREIGN KEY (`tstgrp_group_id`) REFERENCES `tce_user_groups` (`group_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_testgroups`
--

LOCK TABLES `tce_testgroups` WRITE;
/*!40000 ALTER TABLE `tce_testgroups` DISABLE KEYS */;
INSERT INTO `tce_testgroups` VALUES (1,2);
/*!40000 ALTER TABLE `tce_testgroups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_tests`
--

DROP TABLE IF EXISTS `tce_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_tests` (
  `test_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `test_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `test_description` text COLLATE utf8_unicode_ci NOT NULL,
  `test_begin_time` datetime DEFAULT NULL,
  `test_end_time` datetime DEFAULT NULL,
  `test_duration_time` smallint(10) unsigned NOT NULL DEFAULT '0',
  `test_ip_range` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '*.*.*.*',
  `test_results_to_users` tinyint(1) NOT NULL DEFAULT '0',
  `test_report_to_users` tinyint(1) NOT NULL DEFAULT '0',
  `test_score_right` decimal(10,3) DEFAULT '1.000',
  `test_score_wrong` decimal(10,3) DEFAULT '0.000',
  `test_score_unanswered` decimal(10,3) DEFAULT '0.000',
  `test_max_score` decimal(10,3) NOT NULL DEFAULT '0.000',
  `test_user_id` bigint(20) unsigned NOT NULL DEFAULT '1',
  `test_score_threshold` decimal(10,3) DEFAULT '0.000',
  `test_random_questions_select` tinyint(1) NOT NULL DEFAULT '1',
  `test_random_questions_order` tinyint(1) NOT NULL DEFAULT '1',
  `test_questions_order_mode` smallint(3) unsigned NOT NULL DEFAULT '0',
  `test_random_answers_select` tinyint(1) NOT NULL DEFAULT '1',
  `test_random_answers_order` tinyint(1) NOT NULL DEFAULT '1',
  `test_answers_order_mode` smallint(3) unsigned NOT NULL DEFAULT '0',
  `test_comment_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `test_menu_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `test_noanswer_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `test_mcma_radio` tinyint(1) NOT NULL DEFAULT '1',
  `test_repeatable` tinyint(1) NOT NULL DEFAULT '0',
  `test_mcma_partial_score` tinyint(1) NOT NULL DEFAULT '1',
  `test_logout_on_timeout` tinyint(1) NOT NULL DEFAULT '0',
  `test_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`test_id`),
  UNIQUE KEY `ak_test_name` (`test_name`),
  KEY `p_test_user_id` (`test_user_id`),
  CONSTRAINT `tce_tests_ibfk_1` FOREIGN KEY (`test_user_id`) REFERENCES `tce_users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_tests`
--

LOCK TABLES `tce_tests` WRITE;
/*!40000 ALTER TABLE `tce_tests` DISABLE KEYS */;
INSERT INTO `tce_tests` VALUES (1,'test - informatika','test za njubove','2015-04-06 02:47:51','2015-05-30 02:47:51',2048,'*.*.*.*',1,1,1.000,0.000,0.000,6.000,2,4.000,1,1,0,1,1,0,1,1,1,1,1,1,0,NULL);
/*!40000 ALTER TABLE `tce_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_tests_logs`
--

DROP TABLE IF EXISTS `tce_tests_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_tests_logs` (
  `testlog_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `testlog_testuser_id` bigint(20) unsigned NOT NULL,
  `testlog_user_ip` varchar(39) COLLATE utf8_unicode_ci DEFAULT NULL,
  `testlog_question_id` bigint(20) unsigned NOT NULL,
  `testlog_answer_text` text COLLATE utf8_unicode_ci,
  `testlog_score` decimal(10,3) DEFAULT NULL,
  `testlog_creation_time` datetime DEFAULT NULL,
  `testlog_display_time` datetime DEFAULT NULL,
  `testlog_change_time` datetime DEFAULT NULL,
  `testlog_reaction_time` bigint(20) unsigned NOT NULL DEFAULT '0',
  `testlog_order` smallint(6) NOT NULL DEFAULT '1',
  `testlog_num_answers` smallint(5) unsigned NOT NULL DEFAULT '0',
  `testlog_comment` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`testlog_id`),
  UNIQUE KEY `ak_testuser_question` (`testlog_testuser_id`,`testlog_question_id`),
  KEY `p_testlog_question_id` (`testlog_question_id`),
  KEY `p_testlog_testuser_id` (`testlog_testuser_id`),
  CONSTRAINT `tce_tests_logs_ibfk_1` FOREIGN KEY (`testlog_question_id`) REFERENCES `tce_questions` (`question_id`) ON UPDATE NO ACTION,
  CONSTRAINT `tce_tests_logs_ibfk_2` FOREIGN KEY (`testlog_testuser_id`) REFERENCES `tce_tests_users` (`testuser_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_tests_logs`
--

LOCK TABLES `tce_tests_logs` WRITE;
/*!40000 ALTER TABLE `tce_tests_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_tests_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_tests_logs_answers`
--

DROP TABLE IF EXISTS `tce_tests_logs_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_tests_logs_answers` (
  `logansw_testlog_id` bigint(20) unsigned NOT NULL,
  `logansw_answer_id` bigint(20) unsigned NOT NULL,
  `logansw_selected` smallint(6) NOT NULL DEFAULT '-1',
  `logansw_order` smallint(6) NOT NULL DEFAULT '1',
  `logansw_position` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`logansw_testlog_id`,`logansw_answer_id`),
  KEY `p_logansw_answer_id` (`logansw_answer_id`),
  KEY `p_logansw_testlog_id` (`logansw_testlog_id`),
  CONSTRAINT `tce_tests_logs_answers_ibfk_1` FOREIGN KEY (`logansw_answer_id`) REFERENCES `tce_answers` (`answer_id`) ON UPDATE NO ACTION,
  CONSTRAINT `tce_tests_logs_answers_ibfk_2` FOREIGN KEY (`logansw_testlog_id`) REFERENCES `tce_tests_logs` (`testlog_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_tests_logs_answers`
--

LOCK TABLES `tce_tests_logs_answers` WRITE;
/*!40000 ALTER TABLE `tce_tests_logs_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_tests_logs_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_tests_users`
--

DROP TABLE IF EXISTS `tce_tests_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_tests_users` (
  `testuser_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `testuser_test_id` bigint(20) unsigned NOT NULL,
  `testuser_user_id` bigint(20) unsigned NOT NULL,
  `testuser_status` smallint(5) unsigned NOT NULL DEFAULT '0',
  `testuser_creation_time` datetime NOT NULL,
  `testuser_comment` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`testuser_id`),
  UNIQUE KEY `ak_testuser` (`testuser_test_id`,`testuser_user_id`,`testuser_status`),
  KEY `p_testuser_user_id` (`testuser_user_id`),
  KEY `p_testuser_test_id` (`testuser_test_id`),
  CONSTRAINT `tce_tests_users_ibfk_1` FOREIGN KEY (`testuser_user_id`) REFERENCES `tce_users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `tce_tests_users_ibfk_2` FOREIGN KEY (`testuser_test_id`) REFERENCES `tce_tests` (`test_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_tests_users`
--

LOCK TABLES `tce_tests_users` WRITE;
/*!40000 ALTER TABLE `tce_tests_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_tests_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_testsslcerts`
--

DROP TABLE IF EXISTS `tce_testsslcerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_testsslcerts` (
  `tstssl_test_id` bigint(20) unsigned NOT NULL,
  `tstssl_ssl_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`tstssl_test_id`,`tstssl_ssl_id`),
  KEY `p_tstssl_test_id` (`tstssl_test_id`),
  KEY `p_tstssl_ssl_id` (`tstssl_ssl_id`),
  CONSTRAINT `tce_testsslcerts_ibfk_1` FOREIGN KEY (`tstssl_test_id`) REFERENCES `tce_tests` (`test_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `tce_testsslcerts_ibfk_2` FOREIGN KEY (`tstssl_ssl_id`) REFERENCES `tce_sslcerts` (`ssl_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_testsslcerts`
--

LOCK TABLES `tce_testsslcerts` WRITE;
/*!40000 ALTER TABLE `tce_testsslcerts` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_testsslcerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_testuser_stat`
--

DROP TABLE IF EXISTS `tce_testuser_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_testuser_stat` (
  `tus_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tus_date` datetime NOT NULL,
  PRIMARY KEY (`tus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_testuser_stat`
--

LOCK TABLES `tce_testuser_stat` WRITE;
/*!40000 ALTER TABLE `tce_testuser_stat` DISABLE KEYS */;
/*!40000 ALTER TABLE `tce_testuser_stat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_user_groups`
--

DROP TABLE IF EXISTS `tce_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_user_groups` (
  `group_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_user_groups`
--

LOCK TABLES `tce_user_groups` WRITE;
/*!40000 ALTER TABLE `tce_user_groups` DISABLE KEYS */;
INSERT INTO `tce_user_groups` VALUES (1,'default'),(2,'studenti');
/*!40000 ALTER TABLE `tce_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_users`
--

DROP TABLE IF EXISTS `tce_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_users` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `user_password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `user_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_regdate` datetime NOT NULL,
  `user_ip` varchar(39) COLLATE utf8_unicode_ci NOT NULL,
  `user_firstname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_lastname` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_birthdate` date DEFAULT NULL,
  `user_birthplace` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_regnumber` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_ssn` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_level` smallint(3) unsigned NOT NULL DEFAULT '1',
  `user_verifycode` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_otpkey` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `ak_user_name` (`user_name`),
  UNIQUE KEY `user_verifycode` (`user_verifycode`),
  UNIQUE KEY `ak_user_regnumber` (`user_regnumber`),
  UNIQUE KEY `ak_user_ssn` (`user_ssn`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_users`
--

LOCK TABLES `tce_users` WRITE;
/*!40000 ALTER TABLE `tce_users` DISABLE KEYS */;
INSERT INTO `tce_users` VALUES (1,'anonymous','6d068345f42a134a12adddadead25ffd',NULL,'2001-01-01 01:01:01','0.0.0.0',NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL),(2,'admin','c574b5b09ab10f4f39ae9dce6d539cf0',NULL,'2001-01-01 01:01:01','127.0.0.0',NULL,NULL,NULL,NULL,NULL,NULL,10,NULL,NULL),(3,'johndoe','d7819bbf275e268ba6b897b6f7dd313b',NULL,'2015-04-06 02:25:37','0000:0000:0000:0000:0000:ffff:7f00:0001',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,'YRND3QVRADH5WMMD');
/*!40000 ALTER TABLE `tce_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tce_usrgroups`
--

DROP TABLE IF EXISTS `tce_usrgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tce_usrgroups` (
  `usrgrp_user_id` bigint(20) unsigned NOT NULL,
  `usrgrp_group_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`usrgrp_user_id`,`usrgrp_group_id`),
  KEY `p_usrgrp_user_id` (`usrgrp_user_id`),
  KEY `p_usrgrp_group_id` (`usrgrp_group_id`),
  CONSTRAINT `tce_usrgroups_ibfk_1` FOREIGN KEY (`usrgrp_user_id`) REFERENCES `tce_users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `tce_usrgroups_ibfk_2` FOREIGN KEY (`usrgrp_group_id`) REFERENCES `tce_user_groups` (`group_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tce_usrgroups`
--

LOCK TABLES `tce_usrgroups` WRITE;
/*!40000 ALTER TABLE `tce_usrgroups` DISABLE KEYS */;
INSERT INTO `tce_usrgroups` VALUES (2,1),(2,2),(3,2);
/*!40000 ALTER TABLE `tce_usrgroups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-06  3:16:12
