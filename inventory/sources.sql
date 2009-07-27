-- MySQL dump 10.11
--
-- Host: localhost    Database: sources
-- ------------------------------------------------------
-- Server version	5.0.51a-24+lenny1

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
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

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
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_5886d21f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add budget',9,'add_budget'),(26,'Can change budget',9,'change_budget'),(27,'Can delete budget',9,'delete_budget'),(28,'Can add budget category',10,'add_budgetcategory'),(29,'Can change budget category',10,'change_budgetcategory'),(30,'Can delete budget category',10,'delete_budgetcategory'),(31,'Can add budget item',11,'add_budgetitem'),(32,'Can change budget item',11,'change_budgetitem'),(33,'Can delete budget item',11,'delete_budgetitem'),(49,'Can add equipment type',17,'add_equipmenttype'),(48,'Can delete access model',16,'delete_accessmodel'),(46,'Can add access model',16,'add_accessmodel'),(47,'Can change access model',16,'change_accessmodel'),(40,'Can add suggestion',14,'add_suggestion'),(41,'Can change suggestion',14,'change_suggestion'),(42,'Can delete suggestion',14,'delete_suggestion'),(43,'Can add comment',15,'add_comment'),(44,'Can change comment',15,'change_comment'),(45,'Can delete comment',15,'delete_comment'),(50,'Can change equipment type',17,'change_equipmenttype'),(51,'Can delete equipment type',17,'delete_equipmenttype'),(52,'Can add site',18,'add_site'),(53,'Can change site',18,'change_site'),(54,'Can delete site',18,'delete_site'),(55,'Can add equipment',19,'add_equipment'),(56,'Can change equipment',19,'change_equipment'),(57,'Can delete equipment',19,'delete_equipment'),(58,'Can add equipment capability',20,'add_equipmentcapability'),(59,'Can change equipment capability',20,'change_equipmentcapability'),(60,'Can delete equipment capability',20,'delete_equipmentcapability');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'smari','','','smari@anarchism.is','sha1$56e2e$89ac92e6c0ac4d7058567786a49620c0f64c7c52',1,1,1,'2009-06-24 12:41:34','2009-06-24 12:41:08');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f116770` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL auto_increment,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) default NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2009-06-24 12:41:45',1,9,'1','Fjárlög Íslenska ríkisins 2009',1,''),(2,'2009-06-24 12:42:05',1,10,'1','Æðsta stjórn ríkisins',2,'Changed name and parent.'),(3,'2009-06-27 00:01:04',1,16,'1','Commercial',1,''),(4,'2009-06-27 00:01:44',1,16,'2','Open Access',1,''),(5,'2009-06-27 00:02:50',1,16,'3','Fab Lab charter model',1,''),(6,'2009-06-27 00:07:48',1,20,'1','Laser cutter',1,''),(7,'2009-06-27 00:07:59',1,20,'2','3D mill',1,''),(8,'2009-06-27 00:08:07',1,20,'3','pick\'n\'place',1,''),(9,'2009-06-27 00:08:29',1,20,'4','Fuse Deposition Modeling (FDM)',1,''),(10,'2009-06-27 00:08:40',1,20,'5','Stereolithography (SLA)',1,''),(11,'2009-06-27 00:08:55',1,20,'6','Knitting',1,''),(12,'2009-06-27 00:09:16',1,20,'7','Lathe',1,''),(13,'2009-06-27 00:09:44',1,20,'8','Vinil cutter',1,''),(14,'2009-06-27 00:09:49',1,20,'9','Laser printer',1,''),(15,'2009-06-27 00:09:54',1,20,'10','Inkjet printer',1,''),(16,'2009-06-27 00:10:02',1,20,'11','Computer',1,''),(17,'2009-06-27 00:13:33',1,17,'1','Epilog Mini 24x12',1,''),(18,'2009-06-27 00:14:07',1,17,'2','Shopbot Tools Shopbot PRS Alpha',1,''),(19,'2009-06-27 00:14:26',1,17,'3','Roland Modela MDX-20',1,''),(20,'2009-06-27 00:15:09',1,17,'4','Roland CAMM-1',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'log entry','admin','logentry'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'budget','fjarlog','budget'),(10,'budget category','fjarlog','budgetcategory'),(11,'budget item','fjarlog','budgetitem'),(16,'access model','fabmap','accessmodel'),(14,'suggestion','fjarlog','suggestion'),(15,'comment','fjarlog','comment'),(17,'equipment type','fabmap','equipmenttype'),(18,'site','fabmap','site'),(19,'equipment','fabmap','equipment'),(20,'equipment capability','fabmap','equipmentcapability');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY  (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('a915e8307ad233bbdd69749e09c88dc4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS40OGQ3NTdiMmI5YWQyMzMzMzkw\nMGQ3MDc3ZTcwNTE3OA==\n','2009-07-08 12:41:34');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL auto_increment,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_accessmodel`
--

DROP TABLE IF EXISTS `fabmap_accessmodel`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_accessmodel` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_accessmodel`
--

LOCK TABLES `fabmap_accessmodel` WRITE;
/*!40000 ALTER TABLE `fabmap_accessmodel` DISABLE KEYS */;
INSERT INTO `fabmap_accessmodel` VALUES (1,'Commercial','Pay for access to equipment'),(2,'Open Access','Free access to equipment, will frequently accept donations or require participation to some degree.'),(3,'Fab Lab charter model','Similar to Open Access models, but are guided by a the following charter:\r\n\r\nThe Fab Charter\r\n\r\n\r\nMission: fab labs are a global network of local labs, enabling invention by providing access for individuals to tools for digital fabrication.\r\n\r\nAccess: you can use the fab lab to make almost anything (that doesn\'t hurt anyone); you must learn to do it yourself, and you must share use of the lab with other uses and users\r\n\r\nEducation: training in the fab lab is based on doing projects and learning from peers; you\'re expected to contribute to documentation and instruction\r\n\r\nResponsibility: you\'re responsible for:\r\n\r\nsafety: knowing how to work without hurting people or machines\r\ncleaning up: leaving the lab cleaner than you found it\r\noperations: assisting with maintaining, repairing, and reporting on tools, supplies, and incidents\r\n\r\nSecrecy: designs and processes developed in fab labs must remain available for individual use although intellectual property can be protected however you choose\r\n\r\nBusiness: commercial activities can be incubated in fab labs but they must not conflict with open access, they should grow beyond rather than within the lab, and they are expected to benefit the inventors, labs, and networks that contribute to their success.\r\n');
/*!40000 ALTER TABLE `fabmap_accessmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_equipment`
--

DROP TABLE IF EXISTS `fabmap_equipment`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_equipment` (
  `id` int(11) NOT NULL auto_increment,
  `type_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  `notes` longtext NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `fabmap_equipment_type_id` (`type_id`),
  KEY `fabmap_equipment_site_id` (`site_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_equipment`
--

LOCK TABLES `fabmap_equipment` WRITE;
/*!40000 ALTER TABLE `fabmap_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `fabmap_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_equipmentcapability`
--

DROP TABLE IF EXISTS `fabmap_equipmentcapability`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_equipmentcapability` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_equipmentcapability`
--

LOCK TABLES `fabmap_equipmentcapability` WRITE;
/*!40000 ALTER TABLE `fabmap_equipmentcapability` DISABLE KEYS */;
INSERT INTO `fabmap_equipmentcapability` VALUES (1,'Laser cutter'),(2,'3D mill'),(3,'pick\'n\'place'),(4,'Fuse Deposition Modeling (FDM)'),(5,'Stereolithography (SLA)'),(6,'Knitting'),(7,'Lathe'),(8,'Vinil cutter'),(9,'Laser printer'),(10,'Inkjet printer'),(11,'Computer');
/*!40000 ALTER TABLE `fabmap_equipmentcapability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_equipmenttype`
--

DROP TABLE IF EXISTS `fabmap_equipmenttype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_equipmenttype` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  `maker` varchar(200) NOT NULL,
  `website` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_equipmenttype`
--

LOCK TABLES `fabmap_equipmenttype` WRITE;
/*!40000 ALTER TABLE `fabmap_equipmenttype` DISABLE KEYS */;
INSERT INTO `fabmap_equipmenttype` VALUES (1,'Mini 24x12','Epilog','http://www.epiloglaser.com/'),(2,'Shopbot PRS Alpha','Shopbot Tools','http://www.shopbottools.com/'),(3,'Modela MDX-20','Roland',''),(4,'CAMM-1','Roland','');
/*!40000 ALTER TABLE `fabmap_equipmenttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_equipmenttype_capabilities`
--

DROP TABLE IF EXISTS `fabmap_equipmenttype_capabilities`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_equipmenttype_capabilities` (
  `id` int(11) NOT NULL auto_increment,
  `equipmenttype_id` int(11) NOT NULL,
  `equipmentcapability_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `equipmenttype_id` (`equipmenttype_id`,`equipmentcapability_id`),
  KEY `equipmentcapability_id_refs_id_45ca1995` (`equipmentcapability_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_equipmenttype_capabilities`
--

LOCK TABLES `fabmap_equipmenttype_capabilities` WRITE;
/*!40000 ALTER TABLE `fabmap_equipmenttype_capabilities` DISABLE KEYS */;
INSERT INTO `fabmap_equipmenttype_capabilities` VALUES (1,1,1),(2,2,2),(3,3,2),(4,4,8);
/*!40000 ALTER TABLE `fabmap_equipmenttype_capabilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabmap_site`
--

DROP TABLE IF EXISTS `fabmap_site`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fabmap_site` (
  `id` int(11) NOT NULL auto_increment,
  `lat` double NOT NULL,
  `lon` double NOT NULL,
  `name` varchar(200) NOT NULL,
  `locname` varchar(200) NOT NULL,
  `website` varchar(200) NOT NULL,
  `manager_id` int(11) NOT NULL,
  `access_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `fabmap_site_manager_id` (`manager_id`),
  KEY `fabmap_site_access_id` (`access_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fabmap_site`
--

LOCK TABLES `fabmap_site` WRITE;
/*!40000 ALTER TABLE `fabmap_site` DISABLE KEYS */;
/*!40000 ALTER TABLE `fabmap_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fjarlog_budget`
--

DROP TABLE IF EXISTS `fjarlog_budget`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fjarlog_budget` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fjarlog_budget`
--

LOCK TABLES `fjarlog_budget` WRITE;
/*!40000 ALTER TABLE `fjarlog_budget` DISABLE KEYS */;
INSERT INTO `fjarlog_budget` VALUES (1,'Fjárlög Íslenska ríkisins 2009');
/*!40000 ALTER TABLE `fjarlog_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fjarlog_budgetcategory`
--

DROP TABLE IF EXISTS `fjarlog_budgetcategory`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fjarlog_budgetcategory` (
  `id` int(11) NOT NULL auto_increment,
  `budget_id` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `name` varchar(200) NOT NULL,
  `parent_id` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `fjarlog_budgetcategory_budget_id` (`budget_id`),
  KEY `fjarlog_budgetcategory_parent_id` (`parent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fjarlog_budgetcategory`
--

LOCK TABLES `fjarlog_budgetcategory` WRITE;
/*!40000 ALTER TABLE `fjarlog_budgetcategory` DISABLE KEYS */;
INSERT INTO `fjarlog_budgetcategory` VALUES (1,1,'00','Æðsta stjórn ríkisins',NULL),(2,1,'01','Forsætisráðuneyti',NULL),(3,1,'02','Menntamálaráðuneyti',NULL),(4,1,'03','Utanríkisráðuneyti',NULL),(5,1,'04','Sjávarútvegs- og landbúnaðarráðuneyti',NULL),(6,1,'06','Dóms- og kirkjumálaráðuneyti',NULL),(7,1,'07','Félags- og tryggingamálaráðuneyti',NULL),(8,1,'08','Heilbrigðisráðuneyti',NULL),(9,1,'09','Fjármálaráðuneyti',NULL),(10,1,'10','Samgönguráðuneyti',NULL),(11,1,'11','Iðnaðarráðuneyti',NULL),(12,1,'12','Viðskiptaráðuneyti',NULL),(13,1,'14','Umhverfisráðuneyti',NULL),(14,1,'19','Vaxtagjöld ríkissjóðs',NULL);
/*!40000 ALTER TABLE `fjarlog_budgetcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fjarlog_budgetitem`
--

DROP TABLE IF EXISTS `fjarlog_budgetitem`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fjarlog_budgetitem` (
  `id` int(11) NOT NULL auto_increment,
  `code` varchar(10) NOT NULL,
  `name` varchar(200) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `funds` double NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `fjarlog_budgetitem_parent_id` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fjarlog_budgetitem`
--

LOCK TABLES `fjarlog_budgetitem` WRITE;
/*!40000 ALTER TABLE `fjarlog_budgetitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `fjarlog_budgetitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fjarlog_comment`
--

DROP TABLE IF EXISTS `fjarlog_comment`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fjarlog_comment` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `comment` longtext NOT NULL,
  `attachment` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `fjarlog_comment_user_id` (`user_id`),
  KEY `fjarlog_comment_item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fjarlog_comment`
--

LOCK TABLES `fjarlog_comment` WRITE;
/*!40000 ALTER TABLE `fjarlog_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `fjarlog_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fjarlog_suggestion`
--

DROP TABLE IF EXISTS `fjarlog_suggestion`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fjarlog_suggestion` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `funds` double NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `fjarlog_suggestion_user_id` (`user_id`),
  KEY `fjarlog_suggestion_item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Dumping data for table `fjarlog_suggestion`
--

LOCK TABLES `fjarlog_suggestion` WRITE;
/*!40000 ALTER TABLE `fjarlog_suggestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `fjarlog_suggestion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2009-06-28 16:20:49
