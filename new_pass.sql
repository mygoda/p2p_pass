-- MySQL dump 10.13  Distrib 5.7.10, for osx10.11 (x86_64)
--
-- Host: 172.16.0.171    Database: paas
-- ------------------------------------------------------
-- Server version	5.5.5-10.0.21-MariaDB-1~trusty-wsrep-log

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add content type',3,'add_contenttype'),(8,'Can change content type',3,'change_contenttype'),(9,'Can delete content type',3,'delete_contenttype'),(10,'Can add session',4,'add_session'),(11,'Can change session',4,'change_session'),(12,'Can delete session',4,'delete_session'),(13,'Can add site',5,'add_site'),(14,'Can change site',5,'change_site'),(15,'Can delete site',5,'delete_site'),(16,'Can add log entry',6,'add_logentry'),(17,'Can change log entry',6,'change_logentry'),(18,'Can delete log entry',6,'delete_logentry'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add 虚拟机性能',8,'add_vmstat'),(23,'Can change 虚拟机性能',8,'change_vmstat'),(24,'Can delete 虚拟机性能',8,'delete_vmstat'),(25,'Can add 数据中心',9,'add_vcenter'),(26,'Can change 数据中心',9,'change_vcenter'),(27,'Can delete 数据中心',9,'delete_vcenter'),(28,'Can add 任务',10,'add_task'),(29,'Can change 任务',10,'change_task'),(30,'Can delete 任务',10,'delete_task'),(31,'Can add 用户',11,'add_user'),(32,'Can change 用户',11,'change_user'),(33,'Can delete 用户',11,'delete_user'),(34,'Can add task state',12,'add_taskmeta'),(35,'Can change task state',12,'change_taskmeta'),(36,'Can delete task state',12,'delete_taskmeta'),(37,'Can add saved group result',13,'add_tasksetmeta'),(38,'Can change saved group result',13,'change_tasksetmeta'),(39,'Can delete saved group result',13,'delete_tasksetmeta'),(40,'Can add interval',14,'add_intervalschedule'),(41,'Can change interval',14,'change_intervalschedule'),(42,'Can delete interval',14,'delete_intervalschedule'),(43,'Can add crontab',15,'add_crontabschedule'),(44,'Can change crontab',15,'change_crontabschedule'),(45,'Can delete crontab',15,'delete_crontabschedule'),(46,'Can add periodic tasks',16,'add_periodictasks'),(47,'Can change periodic tasks',16,'change_periodictasks'),(48,'Can delete periodic tasks',16,'delete_periodictasks'),(49,'Can add periodic task',17,'add_periodictask'),(50,'Can change periodic task',17,'change_periodictask'),(51,'Can delete periodic task',17,'delete_periodictask'),(52,'Can add worker',18,'add_workerstate'),(53,'Can change worker',18,'change_workerstate'),(54,'Can delete worker',18,'delete_workerstate'),(55,'Can add task',19,'add_taskstate'),(56,'Can change task',19,'change_taskstate'),(57,'Can delete task',19,'delete_taskstate');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_74953f86` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-05-03 03:00:03',1,9,'1','YFCLOUD',1,''),(2,'2016-06-28 04:33:41',1,10,'75','90fa05a2-3cd5-11e6-89d9-dc5360378c14',2,'已修改 params，result 和 status 。'),(3,'2016-06-30 06:22:27',1,10,'75','90fa05a2-3cd5-11e6-89d9-dc5360378c14',2,'已修改 params，result 和 status 。'),(4,'2016-07-04 06:26:16',1,10,'85','116301c4-41b0-11e6-beb3-0242ac110006',3,''),(5,'2016-07-04 06:26:16',1,10,'84','116301c4-41b0-11e6-beb3-0242ac110006',3,''),(6,'2016-07-04 06:27:37',1,10,'87','4d99c592-41b0-11e6-99d8-0242ac110006',3,''),(7,'2016-07-04 06:27:37',1,10,'86','4d99c592-41b0-11e6-99d8-0242ac110006',3,''),(8,'2016-07-04 08:22:22',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(9,'2016-07-04 08:25:24',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(10,'2016-07-04 08:28:17',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(11,'2016-07-04 08:34:38',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(12,'2016-07-04 08:36:03',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(13,'2016-07-04 08:54:21',1,10,'109','3e1b5918-41bb-11e6-a547-0242ac110006',2,'已修改 params 和 result 。'),(14,'2016-07-05 01:19:44',1,9,'2','POD09(CNPEK-ZW)',2,'已修改 capacity 。'),(15,'2016-07-05 01:23:50',1,9,'2','POD09(CNPEK-ZW)',2,'没有字段被修改。'),(16,'2016-07-05 01:25:40',1,9,'4','POD10(CNWUX-CL)',1,''),(17,'2016-07-05 01:28:14',1,9,'4','POD10(CNWUX-CL)',2,'已修改 host，username，password，ovf_agent_host 和 ovf_agent_port 。'),(18,'2016-07-05 01:30:20',1,9,'4','POD10(CNWUX-CL)',2,'已修改 data_center，data_store，cluster_name，p2p_center_host，p2p_center_port 和 capacity 。'),(19,'2016-07-05 01:32:09',1,9,'5','POD11(SGSIN-SG3)',1,''),(20,'2016-07-05 01:32:19',1,9,'4','POD10(CNWUX-CL)',2,'已修改 p2p_center_host 。'),(21,'2016-07-05 01:34:58',1,9,'6','POD12(DEFRA-FR4)',1,''),(22,'2016-07-05 01:37:06',1,9,'7','POD13(USLAX-CT)',1,''),(23,'2016-07-05 01:38:42',1,9,'8','POD14(CNPEK-MJQ)',1,''),(24,'2016-07-05 01:40:14',1,9,'9','POD15(USNYC-NY2)',1,''),(25,'2016-07-05 01:42:00',1,9,'10','POD16(CNPEK-QNL)',1,''),(26,'2016-07-05 01:43:35',1,9,'11','POD17(CNHKG-HK2)',1,''),(27,'2016-07-05 01:47:41',1,9,'12','POD08(JPTKY-TY4)',1,''),(28,'2016-07-05 01:49:57',1,9,'13','POD06(USDAL-DB)',1,''),(29,'2016-07-06 05:24:37',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(30,'2016-07-06 05:26:48',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(31,'2016-07-06 05:29:48',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(32,'2016-07-06 05:33:20',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(33,'2016-07-06 05:35:28',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(34,'2016-07-06 05:45:37',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(35,'2016-07-06 05:53:47',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(36,'2016-07-06 05:55:46',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(37,'2016-07-06 06:04:55',1,10,'142','ce504bae-42da-11e6-bea0-dc5360378c14',2,'已修改 params，result 和 status 。'),(38,'2016-07-06 06:06:15',1,10,'142','ce504bae-42da-11e6-bea0-dc5360378c14',2,'已修改 params，result 和 status 。'),(39,'2016-07-06 06:11:17',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(40,'2016-07-06 06:13:28',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(41,'2016-07-06 06:15:18',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(42,'2016-07-06 06:15:39',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params 和 result 。'),(43,'2016-07-06 06:15:49',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(44,'2016-07-06 06:17:26',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(45,'2016-07-06 06:19:11',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(46,'2016-07-06 06:24:34',1,10,'158','05c4f0b2-4326-11e6-910b-0242ac110006',2,'已修改 params，result 和 status 。'),(47,'2016-07-07 01:10:38',1,14,'1','every 3 minutes',1,''),(48,'2016-07-07 01:10:41',1,17,'1','check_data_store: every 3 minutes',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'content type','contenttypes','contenttype'),(4,'session','sessions','session'),(5,'site','sites','site'),(6,'log entry','admin','logentry'),(7,'migration history','south','migrationhistory'),(8,'虚拟机性能','stat','vmstat'),(9,'数据中心','stat','vcenter'),(10,'任务','stat','task'),(11,'用户','users','user'),(12,'task state','djcelery','taskmeta'),(13,'saved group result','djcelery','tasksetmeta'),(14,'interval','djcelery','intervalschedule'),(15,'crontab','djcelery','crontabschedule'),(16,'periodic tasks','djcelery','periodictasks'),(17,'periodic task','djcelery','periodictask'),(18,'worker','djcelery','workerstate'),(19,'task','djcelery','taskstate');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('9gy4qbcy29h5o4v9iraz8ti9t3q7fjis','ZDI0NDg2NWFlMTBiYWM3NDJhYWI0MzRmMjNmNmE1NGMwYWRiNDhhOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcGxpY2F0aW9ucy51c2Vycy5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoxfQ==','2019-05-03 02:58:32'),('ao37rdhbrgr195v7gb2ajnjxka0y37zf','ZDI0NDg2NWFlMTBiYWM3NDJhYWI0MzRmMjNmNmE1NGMwYWRiNDhhOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcGxpY2F0aW9ucy51c2Vycy5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoxfQ==','2019-05-03 02:58:32');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
INSERT INTO `djcelery_intervalschedule` VALUES (1,3,'minutes');
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictask_8905f60d` (`interval_id`),
  KEY `djcelery_periodictask_7280124f` (`crontab_id`),
  CONSTRAINT `crontab_id_refs_id_286da0d1` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `interval_id_refs_id_1829f358` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
INSERT INTO `djcelery_periodictask` VALUES (1,'check_data_store','applications.stat.tasks.check_datastore_status',1,NULL,'[]','{}',NULL,NULL,NULL,NULL,0,NULL,0,'2016-07-07 01:10:41','');
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
INSERT INTO `djcelery_periodictasks` VALUES (1,'2016-07-07 01:10:41');
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_5654bf12` (`state`),
  KEY `djcelery_taskstate_4da47e07` (`name`),
  KEY `djcelery_taskstate_abaacd02` (`tstamp`),
  KEY `djcelery_taskstate_cac6a03d` (`worker_id`),
  KEY `djcelery_taskstate_2ff6b945` (`hidden`),
  CONSTRAINT `worker_id_refs_id_6fd8ce95` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_11e400ef` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'django_extensions','0001_empty','2016-05-03 02:57:17'),(2,'djcelery','0001_initial','2016-05-03 02:57:19'),(3,'djcelery','0002_v25_changes','2016-05-03 02:57:22'),(4,'djcelery','0003_v26_changes','2016-05-03 02:57:23'),(5,'djcelery','0004_v30_changes','2016-05-03 02:57:24');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `phone` varchar(24) DEFAULT NULL,
  `gender` smallint(6) NOT NULL,
  `department` varchar(128) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('pbkdf2_sha256$12000$TR2o67E7ACuJ$5VzJOB0PeVHKwGisB/QFTTMshwiT86jhMovDNLz77As=','2016-05-03 02:58:31',1,1,'1@1.com','',NULL,'',1,'',1,1,1,'2016-05-03 02:56:29');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `user_groups_6340c63c` (`user_id`),
  KEY `user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_7407a5cb` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_720a3f16` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `user_user_permissions_6340c63c` (`user_id`),
  KEY `user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_88d28ac5` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_ccc54e03` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vcenter_info`
--

DROP TABLE IF EXISTS `vcenter_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcenter_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` varchar(32) DEFAULT NULL,
  `host` varchar(16) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `data_center` varchar(32) DEFAULT NULL,
  `data_store` varchar(32) DEFAULT NULL,
  `cluster_name` varchar(32) DEFAULT NULL,
  `ovf_agent_host` varchar(16) DEFAULT NULL,
  `ovf_agent_port` int(11) DEFAULT NULL,
  `p2p_center_host` varchar(16) DEFAULT NULL,
  `p2p_center_port` int(11) DEFAULT NULL,
  `tpl_folder` varchar(32) DEFAULT NULL,
  `site_id` varchar(36) DEFAULT NULL,
  `capacity` float DEFAULT NULL,
  `free_space` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vcenter_info`
--

LOCK TABLES `vcenter_info` WRITE;
/*!40000 ALTER TABLE `vcenter_info` DISABLE KEYS */;
INSERT INTO `vcenter_info` VALUES (1,'YFCLOUD','172.16.0.4','administrator@yf.local','P@$$w0rd','YFCLOUD','H002-Localdisk','YFCLOUD-CLU01','114.112.92.250',5044,'101.251.255.234',9999,NULL,'7422ada0-e280-4702-9fe5-bb8739dfaac5',4,4),(2,'POD09(CNPEK-ZW)','10.128.48.5','api.Adm1n@cdscloud.local','FYb0907','POD09(CNPEK-ZW)','POD09-User-Template','POD09-CLU02','101.251.255.234',5044,'101.251.255.234',9999,'','a18d6c6a-9619-418a-8526-2878f2653d5f',10000,NULL),(4,'POD10(CNWUX-CL)','10.128.40.6','api.Adm1n@cdscloud.local','FYb0907','POD10(CNWUX-CL)','POD10-User-Template','POD10-CLU01','221.228.109.10',5044,'101.251.255.234',9999,'','de0b0931-4c14-4f0b-ab60-7e1768241136',10000,NULL),(5,'POD11(SGSIN-SG3)','10.198.0.4','api.Adm1n@cdscloud.local','FYb0907','POD11(SGSIN-SG3)','POD11-User-Template','POD11-CLU01','118.193.18.138',5044,'101.251.255.234',9999,'','3fd55550-8fd7-4634-84ba-1a9880ec1ce4',10000,NULL),(6,'POD12(DEFRA-FR4)','10.197.0.5','api.Adm1n@cdscloud.local','FYb0907','POD12(DEFRA-FR4)','POD12-User-Template','POD12-CLU02','38.123.104.50',5044,'101.251.255.234',9999,'','1af1d06e-e2ad-41e7-97b0-ed77417fd3d4',5000,NULL),(7,'POD13(USLAX-CT)','10.200.12.4','api.Adm1n@cdscloud.local','FYb0907','POD13(USLAX-CT)','POD13-User-Template','POD13-CLU01','38.121.63.234',5044,'101.251.255.234',9999,'','1a2f0825-ee1b-4c25-9332-e34dd2a621dd',5000,NULL),(8,'POD14(CNPEK-MJQ)','10.128.68.4','api.Adm1n@cdscloud.local','FYb0907','POD14(CNPEK-MJQ)','POD14-User-Template','POD14-CLU01','101.251.214.218',5044,'101.251.255.234',9999,'','843ff9be-b977-4ca1-ab59-d5680caa9b94',10000,NULL),(9,'POD15(USNYC-NY2)','10.200.20.4','api.Adm1n@cdscloud.local','FYb0907','POD15(USNYC-NY2)','POD15-User-Template','POD15-CLU01','148.153.11.26',5044,'101.251.255.234',9999,'','61fb444a-f0ad-41cf-aef2-19297c7dbf37',5000,NULL),(10,'POD16(CNPEK-QNL)','10.128.84.4','api.Adm1n@cdscloud.local','FYb0907','POD16(CNPEK-QNL)','POD16-User-Template','POD16-CLU01','101.251.237.146',5044,'101.251.255.234',9999,'','fdd523fe-fe6c-434a-a817-9b415a0206e8',10000,NULL),(11,'POD17(CNHKG-HK2)','10.128.92.4','api.Adm1n@cdscloud.local','FYb0907','POD17(CNHKG-HK2)','POD17-User-Template','POD17-CLU01','223.255.249.2',5044,'101.251.255.234',9999,'','35304122-8504-400c-a61c-56ba244c5dda',5000,NULL),(12,'POD08(JPTKY-TY4)','10.199.0.5','api.Adm1n@cdscloud.local','FYb0907','POD08(JPTKY-TY4)','POD08-User-Template','POD08-CLU01','118.193.16.34',5044,'101.251.255.234',9999,'','31f105b5-389e-4989-9944-8ecf76e9d764',5000,NULL),(13,'POD06(USDAL-DB)','10.200.4.3','api.Adm1n@cdscloud.local','FYb0907','POD06(USDAL-DB)','POD06-User-Template','POD06-CLU04','38.83.108.74',5044,'101.251.255.234',9999,'','b4d0a486-71b3-4e6c-a136-2c9beb98546f',5000,NULL);
/*!40000 ALTER TABLE `vcenter_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vcenter_task`
--

DROP TABLE IF EXISTS `vcenter_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcenter_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(64) DEFAULT NULL,
  `params` longtext,
  `result` longtext,
  `status` varchar(16) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vcenter_task`
--

LOCK TABLES `vcenter_task` WRITE;
/*!40000 ALTER TABLE `vcenter_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `vcenter_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vm_stat`
--

DROP TABLE IF EXISTS `vm_stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vm_stat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vm_name` varchar(1024) DEFAULT '',
  `data` longtext,
  `result` longtext,
  `status` varchar(16) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vm_stat`
--

LOCK TABLES `vm_stat` WRITE;
/*!40000 ALTER TABLE `vm_stat` DISABLE KEYS */;
INSERT INTO `vm_stat` VALUES (1,'E003294-centos6.364-20160629101621-2FXC7JVW','{\"pod_name\": \"YFCLOUD\"}','{\"stat_data\": {\"mem\": [25.65583899905673, 0.0, 12.826389999170724, 0.0, 0.0], \"disk_write\": [0.0, 0.0, 0.0, 0.0, 0.0], \"disk_read\": [0.0, 0.0, 0.0, 0.0, 0.0], \"cpu\": [3.44, 3.44, 3.4, 3.38, 3.39]}, \"time_data\": [\"2016-06-28 08:00:00\", \"2016-06-28 14:00:00\", \"2016-06-28 20:00:00\", \"2016-06-29 02:00:00\", \"2016-06-29 08:00:00\"]}','success','2016-06-28 08:47:40'),(2,'YAFA_TEST-172-16-0-193-CORE','{\"pod_name\": \"YFCLOUD\"}','{\"stat_data\": {\"mem\": [34.21, 34.21, 85.53, 0.0, 0.0, 0.0, 51.32, 0.0, 34.21, 119.74], \"disk_write\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"disk_read\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"cpu\": [0.13, 0.13, 0.11, 0.13, 0.12, 0.13, 0.13, 0.12, 0.11, 0.12]}, \"time_data\": [\"2016-05-09 08:00:00\", \"2016-05-09 16:00:00\", \"2016-05-10 00:00:00\", \"2016-05-10 08:00:00\", \"2016-05-10 16:00:00\", \"2016-05-11 00:00:00\", \"2016-05-11 08:00:00\", \"2016-05-11 16:00:00\", \"2016-05-12 00:00:00\", \"2016-05-12 08:00:00\"]}','success','2016-07-05 07:33:22'),(3,'YAFA_TEST-172-16-0-193-CORE','{\"pod_name\": \"YFCLOUD\"}','{\"stat_data\": {\"mem\": [34.21, 34.21, 85.53, 0.0, 0.0, 0.0, 51.32, 0.0, 34.21, 119.74], \"disk_write\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"disk_read\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"cpu\": [0.13, 0.13, 0.11, 0.13, 0.12, 0.13, 0.13, 0.12, 0.11, 0.12]}, \"time_data\": [\"2016-05-09 08:00:00\", \"2016-05-09 16:00:00\", \"2016-05-10 00:00:00\", \"2016-05-10 08:00:00\", \"2016-05-10 16:00:00\", \"2016-05-11 00:00:00\", \"2016-05-11 08:00:00\", \"2016-05-11 16:00:00\", \"2016-05-12 00:00:00\", \"2016-05-12 08:00:00\"]}','success','2016-07-05 07:33:22'),(4,'YAFA_TEST-172-16-0-193-CORE','{\"pod_name\": \"YFCLOUD\"}','{\"stat_data\": {\"mem\": [34.21, 34.21, 85.53, 0.0, 0.0, 0.0, 51.32, 0.0, 34.21, 119.74], \"disk_write\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"disk_read\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"cpu\": [0.13, 0.13, 0.11, 0.13, 0.12, 0.13, 0.13, 0.12, 0.11, 0.12]}, \"time_data\": [\"2016-05-09 08:00:00\", \"2016-05-09 16:00:00\", \"2016-05-10 00:00:00\", \"2016-05-10 08:00:00\", \"2016-05-10 16:00:00\", \"2016-05-11 00:00:00\", \"2016-05-11 08:00:00\", \"2016-05-11 16:00:00\", \"2016-05-12 00:00:00\", \"2016-05-12 08:00:00\"]}','success','2016-07-05 07:33:22'),(5,'YAFA_TEST-172-16-0-193-CORE','{\"pod_name\": \"YFCLOUD\"}','{\"stat_data\": {\"mem\": [34.21, 34.21, 85.53, 0.0, 0.0, 0.0, 51.32, 0.0, 34.21, 119.74], \"disk_write\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"disk_read\": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \"cpu\": [0.13, 0.13, 0.11, 0.13, 0.12, 0.13, 0.13, 0.12, 0.11, 0.12]}, \"time_data\": [\"2016-05-09 08:00:00\", \"2016-05-09 16:00:00\", \"2016-05-10 00:00:00\", \"2016-05-10 08:00:00\", \"2016-05-10 16:00:00\", \"2016-05-11 00:00:00\", \"2016-05-11 08:00:00\", \"2016-05-11 16:00:00\", \"2016-05-12 00:00:00\", \"2016-05-12 08:00:00\"]}','success','2016-07-05 07:33:22');
/*!40000 ALTER TABLE `vm_stat` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-07  9:18:26
