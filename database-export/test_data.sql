CREATE DATABASE  IF NOT EXISTS `database_test` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `database_test`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: database_test
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actie`
--

DROP TABLE IF EXISTS `actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actie` (
  `ActieID` int NOT NULL AUTO_INCREMENT,
  `ActieBeschrijving` varchar(250) NOT NULL,
  PRIMARY KEY (`ActieID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COMMENT='[';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'temp meten'),(2,'geluid meten'),(3,'licht meten'),(4,'draai meten'),(5,'fans bewegen'),(6,'button ingedrukt');
/*!40000 ALTER TABLE `actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `DeviceID` int NOT NULL AUTO_INCREMENT,
  `Naam` varchar(45) NOT NULL,
  `Merk` varchar(45) DEFAULT NULL,
  `Beschrijving` varchar(250) DEFAULT NULL,
  `Type` varchar(45) NOT NULL,
  `Aankoopkost` float DEFAULT NULL,
  `Meeteenheid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`DeviceID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'LDR',NULL,'licht sensor','sensor',NULL,'percent'),(2,'Temp sensor',NULL,'temperatuur sensor','sensor',NULL,'graden celcius'),(3,'Geluid sensor','Seed','geuid sensor','sensor',NULL,'decibel'),(4,'Rotary encoder',NULL,'draaiknop','sensor',NULL,NULL),(5,'Fan(s)','Kootek','cooling fans','actuator',NULL,NULL),(6,'Scherm',NULL,'lcd scherm','actuator',NULL,NULL),(7,'Knop(aan/uit)',NULL,'power knop','actuator',NULL,NULL),(8,'Knop(aansturing)',NULL,'knop voor rotary encoder of tem sensor','actuator',NULL,NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `Volgnummer` int NOT NULL AUTO_INCREMENT,
  `Actiedatum` datetime DEFAULT NULL,
  `Waarde` varchar(45) DEFAULT NULL,
  `Commentaar` varchar(45) DEFAULT NULL,
  `DeviceID` int NOT NULL,
  `ActieID` int NOT NULL,
  PRIMARY KEY (`Volgnummer`,`DeviceID`,`ActieID`),
  KEY `fk_Historiek_Device_idx` (`DeviceID`),
  KEY `fk_Historiek_Actie1_idx` (`ActieID`),
  CONSTRAINT `fk_Historiek_Actie1` FOREIGN KEY (`ActieID`) REFERENCES `actie` (`ActieID`),
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`DeviceID`) REFERENCES `device` (`DeviceID`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,'2022-05-24 00:00:00','1','knop indruk',7,6),(2,'2022-05-24 00:00:00','36','graden celcius',2,1),(3,'2022-05-24 00:00:00','40','decibel',3,2),(4,'2022-05-24 00:00:00','70','percent',1,3),(5,'2022-05-24 00:00:00','46','graden celcius',2,1),(6,'2022-05-24 00:00:00','42','decibel',3,2),(7,'2022-05-24 00:00:00','70','percent',1,3),(8,'2022-05-24 00:00:00','54','graden celcius',2,1),(9,'2022-05-24 00:00:00','50','decibel',3,2),(10,'2022-05-24 00:00:00','72','percent',1,3),(11,'2022-05-24 00:00:00','62','graden celcius',2,1),(12,'2022-05-24 00:00:00','70','decibel',3,2),(13,'2022-05-24 00:00:00','73','percent',1,3),(14,'2022-05-24 00:00:00','60','graden celcius',2,1),(15,'2022-05-24 00:00:00','40','decibel',3,2),(16,'2022-05-24 00:00:00','71','percent',1,3),(17,'2022-05-24 00:00:00','56','graden celcius',2,1),(18,'2022-05-24 00:00:00','45','decibel',3,2),(19,'2022-05-24 00:00:00','72','percent',1,3),(20,'2022-05-24 00:00:00','64','graden celcius',2,1),(21,'2022-05-24 00:00:00','43','decibel',3,2),(22,'2022-05-24 00:00:00','73','percent',1,3),(23,'2022-05-24 00:00:00','56','graden celcius',2,1),(24,'2022-05-24 00:00:00','42','decibel',3,2),(25,'2022-05-24 00:00:00','70','percent',1,3),(26,'2022-05-24 00:00:00','69','graden celcius',2,1),(27,'2022-05-24 00:00:00','47','decibel',3,2),(28,'2022-05-24 00:00:00','71','percent',1,3),(29,'2022-05-24 00:00:00','64','graden celcius',2,1),(30,'2022-05-24 00:00:00','59','decibel',3,2),(31,'2022-05-24 00:00:00','72','percent',1,3),(32,'2022-05-24 00:00:00','65','graden celcius',2,1),(33,'2022-05-24 00:00:00','46','decibel',3,2),(34,'2022-05-24 00:00:00','73','percent',1,3),(35,'2022-05-24 00:00:00','57','graden celcius',2,1),(36,'2022-05-24 00:00:00','68','decibel',3,2),(37,'2022-05-24 00:00:00','30','percent',1,3),(38,'2022-05-24 00:00:00','59','graden celcius',2,1),(39,'2022-05-24 00:00:00','43','decibel',3,2),(40,'2022-05-24 00:00:00','32','percent',1,3),(41,'2022-05-24 00:00:00','68','graden celcius',2,1),(42,'2022-05-24 00:00:00','78','decibel',3,2),(43,'2022-05-24 00:00:00','33','percent',1,3),(44,'2022-05-24 00:00:00','70','graden celcius',2,1),(45,'2022-05-24 00:00:00','67','decibel',3,2),(46,'2022-05-24 00:00:00','31','percent',1,3),(47,'2022-05-24 00:00:00','65','graden celcius',2,1),(48,'2022-05-24 00:00:00','46','decibel',3,2),(49,'2022-05-24 00:00:00','35','percent',1,3),(50,'2022-05-24 00:00:00','56','graden celcius',2,1);
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-24 10:47:37
