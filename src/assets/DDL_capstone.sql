-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.27-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for capstone_kpi
CREATE DATABASE IF NOT EXISTS `capstone_kpi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `capstone_kpi`;

-- Dumping structure for table capstone_kpi.assessments
CREATE TABLE IF NOT EXISTS `assessments` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `id_assessment` bigint(20) DEFAULT NULL,
  `assessment_type` varchar(4) DEFAULT NULL,
  `date` bigint(20) DEFAULT NULL,
  `weight` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.courses
CREATE TABLE IF NOT EXISTS `courses` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `module_presentation_length` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.studentassessment
CREATE TABLE IF NOT EXISTS `studentassessment` (
  `id_assessment` bigint(20) DEFAULT NULL,
  `id_student` bigint(20) DEFAULT NULL,
  `date_submitted` bigint(20) DEFAULT NULL,
  `is_banked` bigint(20) DEFAULT NULL,
  `score` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.studentinfo
CREATE TABLE IF NOT EXISTS `studentinfo` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `id_student` bigint(20) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `region` varchar(20) DEFAULT NULL,
  `highest_education` varchar(27) DEFAULT NULL,
  `imd_band` varchar(7) DEFAULT NULL,
  `age_band` varchar(5) DEFAULT NULL,
  `num_of_prev_attempts` bigint(20) DEFAULT NULL,
  `studied_credits` bigint(20) DEFAULT NULL,
  `disability` tinyint(1) DEFAULT NULL,
  `final_result` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.studentregistration
CREATE TABLE IF NOT EXISTS `studentregistration` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `id_student` bigint(20) DEFAULT NULL,
  `date_registration` bigint(20) DEFAULT NULL,
  `date_unregistration` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.studentvle
CREATE TABLE IF NOT EXISTS `studentvle` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `id_student` bigint(20) DEFAULT NULL,
  `id_site` bigint(20) DEFAULT NULL,
  `date` bigint(20) DEFAULT NULL,
  `sum_click` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table capstone_kpi.vle
CREATE TABLE IF NOT EXISTS `vle` (
  `code_module` varchar(3) DEFAULT NULL,
  `code_presentation` varchar(5) DEFAULT NULL,
  `id_student` bigint(20) DEFAULT NULL,
  `date_registration` bigint(20) DEFAULT NULL,
  `date_unregistration` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
