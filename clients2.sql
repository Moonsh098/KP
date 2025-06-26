-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: clients
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `loyalty_status_points` float DEFAULT NULL,
  `loyalty_points` float DEFAULT NULL,
  `loyalty_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Ірина Коваленко','iryna.kovalenko@gmail.com','380971234567','Івана Франка  37',1728,402.5,'Лояльний клієнт'),(2,'Олександр Ткаченко','sasha.tkachenko@ukr.net','380503216789','вул. Городоцька 45',170,127.5,'Новачок'),(3,'Марія Петренко','petrenko.masha@gmail.com','380934567890','Зелена 22',150,112.5,'Новачок'),(4,'Андрій Бондар','andriy.bondar@meta.ua','380673334455','Івана Франка  20',1989,207.5,'Лояльний клієнт'),(5,'Наталія Соловей','natalka.solovey@gmail.com','380987776655','Івана Франка  96',6210,3925,'VIP'),(6,'Катерина Литвин','katya.litvyn@ukr.net','380961119988','Чорновола 22',5000,0,'VIP'),(7,'Олена Сидоренко','olena.sidorenko@bigmir.net','380991234321','Івана Мазепи 45',5204,153,'VIP'),(8,'Михайло Коломойський','mykhailo.kolom@gmail.com','380978665732','Чорновола 56',310,232.5,'Новачок'),(9,'Михайло Коломойський1','mykhailo.kolom1@gmail.com','3809786657321','Чорновола 561',620,465,'Новачок');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loyalty_points_history`
--

DROP TABLE IF EXISTS `loyalty_points_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loyalty_points_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `points` float NOT NULL,
  `points_type` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `loyalty_points_before` float NOT NULL,
  `loyalty_status_before` varchar(50) NOT NULL,
  `loyalty_status_points_before` float NOT NULL,
  `loyalty_points_after` float NOT NULL,
  `loyalty_status_after` varchar(50) NOT NULL,
  `loyalty_status_points_after` float NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `loyalty_points_history_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loyalty_points_history`
--

LOCK TABLES `loyalty_points_history` WRITE;
/*!40000 ALTER TABLE `loyalty_points_history` DISABLE KEYS */;
INSERT INTO `loyalty_points_history` VALUES (1,1,0,'Надано статус','Клієнту надано статус \"Новачок\" при створенні',0,'Новачок',0,0,'Новачок',0,'2025-06-26 14:46:22'),(2,2,0,'Надано статус','Клієнту надано статус \"Новачок\" при створенні',0,'Новачок',0,0,'Новачок',0,'2025-06-26 14:46:54'),(3,3,0,'Надано статус','Клієнту надано статус \"Новачок\" при створенні',0,'Новачок',0,0,'Новачок',0,'2025-06-26 14:47:21'),(4,4,0,'Надано статус','Клієнту надано статус \"Лояльний клієнт\" при створенні',0,'Новачок',0,1500,'Лояльний клієнт',1500,'2025-06-26 14:47:53'),(5,5,0,'Надано статус','Клієнту надано статус \"Лояльний клієнт\" при створенні',0,'Новачок',0,1500,'Лояльний клієнт',1500,'2025-06-26 14:48:44'),(6,6,0,'Надано статус','Клієнту надано статус \"VIP\" при створенні',0,'Новачок',0,5000,'VIP',5000,'2025-06-26 14:52:07'),(7,7,0,'Надано статус','Клієнту надано статус \"VIP\" при створенні',0,'Новачок',0,5000,'VIP',5000,'2025-06-26 14:52:54'),(8,2,67.5,'Зарахування балів','Нараховано 67.50 грн за кешбек на замовлення Стіл Модерн',0,'Новачок',0,67.5,'Новачок',90,'2025-06-26 14:55:30'),(9,2,60,'Зарахування балів','Нараховано 60.00 грн за кешбек на замовлення Крісло Комфорт',67.5,'Новачок',90,127.5,'Новачок',170,'2025-06-26 15:00:28'),(10,4,337.5,'Зарахування балів','Нараховано 337.50 грн за кешбек на замовлення Диван Мілан',0,'Лояльний клієнт',1500,337.5,'Лояльний клієнт',1905,'2025-06-26 15:02:10'),(11,5,3925,'Зарахування балів','Нараховано 3925.00 грн за кешбек на замовлення Шафа-купе Браво',0,'Лояльний клієнт',1500,3925,'VIP',6210,'2025-06-26 15:05:10'),(12,4,-200,'Зняття балів','Використано кешбек для оплати замовлення Стілець Лофт',337.5,'Лояльний клієнт',1905,137.5,'Лояльний клієнт',1905,'2025-06-26 15:06:24'),(13,4,70,'Зарахування балів','Нараховано 70.00 грн за кешбек на замовлення Стілець Лофт',137.5,'Лояльний клієнт',1905,207.5,'Лояльний клієнт',1989,'2025-06-26 15:06:24'),(14,7,153,'Зарахування балів','Нараховано 153.00 грн за кешбек на замовлення Комод Ретро',0,'VIP',5000,153,'VIP',5204,'2025-06-26 15:07:44'),(15,6,742.5,'Зарахування балів','Нараховано 742.50 грн за кешбек на замовлення Ліжко Соната',0,'VIP',5000,742.5,'VIP',5990,'2025-06-26 15:08:34'),(16,6,-742.5,'Зняття балів','Замовлення Ліжко Соната скасовано або зміна оплати',742.5,'VIP',5990,0,'VIP',5000,'2025-06-26 15:08:52'),(17,1,1237.5,'Зарахування балів','Нараховано 1237.50 грн за кешбек на замовлення Ліжко Соната',0,'Новачок',0,1237.5,'Лояльний клієнт',1650,'2025-06-26 15:43:48'),(18,1,-900,'Зняття балів','Використано кешбек для оплати замовлення Крісло Комфорт',1237.5,'Лояльний клієнт',1650,337.5,'Лояльний клієнт',1650,'2025-06-26 15:44:49'),(19,1,65,'Зарахування балів','Нараховано 65.00 грн за кешбек на замовлення Крісло Комфорт',337.5,'Лояльний клієнт',1650,402.5,'Лояльний клієнт',1728,'2025-06-26 15:44:49'),(20,3,112.5,'Зарахування балів','Нараховано 112.50 грн за кешбек на замовлення Крісло Модерн',0,'Новачок',0,112.5,'Новачок',150,'2025-06-26 15:46:17'),(21,8,0,'Надано статус','Клієнту надано статус \"Новачок\" при створенні',0,'Новачок',0,0,'Новачок',0,'2025-06-26 15:57:28'),(22,8,232.5,'Зарахування балів','Нараховано 232.50 грн за кешбек на замовлення Диван Міленіум',0,'Новачок',0,232.5,'Новачок',310,'2025-06-26 15:57:54'),(23,9,0,'Надано статус','Клієнту надано статус \"Новачок\" при створенні',0,'Новачок',0,0,'Новачок',0,'2025-06-26 16:04:41'),(24,9,465,'Зарахування балів','Нараховано 465.00 грн за кешбек на замовлення Диван Міленіум',0,'Новачок',0,465,'Новачок',620,'2025-06-26 16:04:53');
/*!40000 ALTER TABLE `loyalty_points_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `delivery_type` varchar(50) DEFAULT NULL,
  `delivery_address` varchar(200) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `comment` text,
  `payment_status` varchar(50) DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `cashback_used` float DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'Стіл Модерн',1,4500,'2025-06-25 00:00:00','pickup','','Завершено','','оплачено',2,0),(2,'Крісло Комфорт',2,2000,'2025-06-06 00:00:00','pickup','','Завершено','','оплачено',2,0),(3,'Диван Мілан',1,13500,'2025-06-02 00:00:00','delivery','Самбір, Шухевича 25','Очікується','','оплачено',4,0),(4,'Шафа-купе Браво',1,157000,'2025-06-01 00:00:00','pickup','','Завершено','','оплачено',5,0),(5,'Стілець Лофт',4,700,'2025-06-01 00:00:00','pickup','','Завершено',' Оплачено кешбеком: 200 балів','оплачено',4,200),(6,'Комод Ретро',1,3400,'2025-06-12 00:00:00','pickup','','Завершено','','оплачено',7,0),(7,'Ліжко Соната',1,16500,'2025-06-11 00:00:00','pickup','','Скасовано','','оплачено',6,0),(8,'Ліжко Соната',5,16500,'2025-06-15 00:00:00','pickup','','Завершено','','оплачено',1,0),(9,'Крісло Комфорт',2,1300,'2025-06-16 00:00:00','pickup','','Завершено',' Оплачено кешбеком: 900 балів','оплачено',1,900),(10,'Крісло Модерн',3,2500,'2025-06-24 00:00:00','pickup','','Завершено','','оплачено',3,0),(11,'Диван Міленіум',1,15500,'2025-06-20 00:00:00','pickup','','Очікується','','оплачено',8,0),(12,'Диван Міленіум',2,15500,'2025-06-20 00:00:00','pickup','','Очікується','','оплачено',9,0);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(120) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Test','Test',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-26 19:53:40
