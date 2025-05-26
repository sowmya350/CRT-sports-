-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: sports_allocations
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `sport_roles`
--

DROP TABLE IF EXISTS `sport_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sport_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sport_id` int NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `max_slots` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_per_sport` (`sport_id`,`role_name`),
  CONSTRAINT `sport_roles_ibfk_1` FOREIGN KEY (`sport_id`) REFERENCES `sports` (`sportid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sport_roles`
--

LOCK TABLES `sport_roles` WRITE;
/*!40000 ALTER TABLE `sport_roles` DISABLE KEYS */;
INSERT INTO `sport_roles` VALUES (1,1,'Raider',2),(2,1,'Defender',4),(3,1,'Captain',1),(4,2,'Goalkeeper',1),(5,2,'Defender',4),(6,2,'Midfielder',4),(7,2,'Forward',3),(8,3,'Guard',2),(9,3,'Forward',2),(10,3,'Center',1),(11,4,'Batsman',4),(12,4,'Bowler',4),(13,4,'Wicket Keeper',1),(14,4,'Captain',1),(15,5,'Spiker',3),(16,5,'Blocker',2),(17,5,'Libero',1),(18,5,'Setter',1),(19,6,'Singles',1),(20,6,'Doubles',2),(21,7,'Singles',1),(22,7,'Doubles',2),(23,8,'Forward',3),(24,8,'Defender',3),(25,8,'Goalkeeper',1),(26,9,'Setter',2),(27,9,'Attacker',3),(28,10,'Chaser',4),(29,10,'Defender',4),(30,1,'Coach',3);
/*!40000 ALTER TABLE `sport_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-26 15:01:21
