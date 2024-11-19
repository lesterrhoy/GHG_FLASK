-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 16, 2024 at 04:01 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ghg_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `electricity_consumption`
--

CREATE TABLE `electricity_consumption` (
  `id` int(11) NOT NULL,
  `campus` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `month` varchar(255) DEFAULT NULL,
  `quarter` varchar(255) DEFAULT NULL,
  `year` varchar(4) DEFAULT NULL,
  `prev_reading` double DEFAULT NULL,
  `current_reading` double DEFAULT NULL,
  `multiplier` double DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `consumption` double DEFAULT NULL,
  `price_per_kwh` double DEFAULT NULL,
  `kg_co2_per_kwh` double DEFAULT NULL,
  `t_co2_per_kwh` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `electricity_consumption`
--

INSERT INTO `electricity_consumption` (`id`, `campus`, `category`, `month`, `quarter`, `year`, `prev_reading`, `current_reading`, `multiplier`, `total_amount`, `consumption`, `price_per_kwh`, `kg_co2_per_kwh`, `t_co2_per_kwh`) VALUES
(94, 'Lipa', 'Mains', 'January', 'Q1', '2023', 1476, 1502, 350, 145878.04, 9100, 16.03, 6481.02, 6.48),
(95, 'Lipa', 'Mains', 'February', 'Q1', '2023', 1502, 1542, 350, 215246.9, 14000, 15.37, 9970.8, 9.97),
(96, 'Lipa', 'Mains', 'March', 'Q1', '2023', 1542, 1582, 350, 217065.71, 14000, 15.5, 9970.8, 9.97),
(97, 'Lipa', 'Mains', 'April', 'Q2', '2023', 1582, 1629, 350, 249305.45, 16450, 15.16, 11715.69, 11.72),
(98, 'Lipa', 'Mains', 'May', 'Q2', '2023', 1629, 1692, 350, 297081.83, 22050, 13.47, 15704.01, 15.7),
(99, 'Lipa', 'Mains', 'June', 'Q2', '2023', 1692, 1724, 350, 154567.33, 11200, 13.8, 7976.64, 7.98),
(100, 'Lipa', 'Mains', 'July', 'Q3', '2023', 1724, 1764, 350, 171394.17, 14000, 12.24, 9970.8, 9.97),
(101, 'Lipa', 'Mains', 'August', 'Q3', '2023', 1764, 1816, 350, 201399.9, 18200, 11.07, 12962.04, 12.96),
(102, 'Lipa', 'Mains', 'September', 'Q3', '2023', 1816, 1877, 350, 169678.1, 21350, 7.95, 15205.47, 15.21),
(103, 'Lipa', 'Mains', 'October', 'Q4', '2023', 1877, 1928, 350, 190544.88, 17850, 10.67, 12712.77, 12.71),
(104, 'Lipa', 'Mains', 'November', 'Q4', '2023', 1928, 1987, 350, 230853.93, 20650, 11.18, 14706.93, 14.71),
(105, 'Lipa', 'Mains', 'December', 'Q4', '2023', 1987, 2022, 350, 141437.98, 12250, 11.55, 8724.45, 8.72),
(106, 'Lipa', 'Mains', 'January', 'Q1', '2022', 2241, 2291, 350, 151360, 17500, 8.65, 12463.5, 12.46),
(107, 'Lipa', 'Mains', 'February', 'Q1', '2022', 2285, 2337, 350, 201455, 18200, 11.07, 12962.04, 12.96),
(108, 'Lipa', 'Mains', 'March', 'Q1', '2022', 2321, 2373, 350, 191895, 18200, 10.54, 12962.04, 12.96),
(109, 'Lipa', 'Mains', 'April', 'Q2', '2022', 2366, 2417, 350, 232379, 17850, 13.02, 12712.77, 12.71),
(111, 'Lipa', 'Mains', 'May', 'Q2', '2022', 2412, 2462, 350, 172717, 17500, 9.87, 12463.5, 12.46),
(112, 'Lipa', 'Mains', 'June', 'Q2', '2022', 2481, 2533, 350, 175819, 18200, 9.66, 12962.04, 12.96),
(113, 'Lipa', 'Mains', 'July', 'Q3', '2022', 2542, 2592, 350, 232785, 17500, 13.3, 12463.5, 12.46),
(114, 'Lipa', 'Mains', 'August', 'Q3', '2022', 2584, 2635, 350, 242910, 17850, 13.61, 12712.77, 12.71),
(115, 'Lipa', 'Mains', 'September', 'Q3', '2022', 2636, 2688, 350, 163495, 18200, 8.98, 12962.04, 12.96),
(116, 'Lipa', 'Mains', 'October', 'Q4', '2022', 2680, 2730, 350, 222726, 17500, 12.73, 12463.5, 12.46),
(117, 'Lipa', 'Mains', 'November', 'Q4', '2022', 2744, 2796, 350, 140561, 18200, 7.72, 12962.04, 12.96),
(118, 'Lipa', 'Mains', 'December', 'Q4', '2022', 2787, 2837, 350, 188412, 17500, 10.77, 12463.5, 12.46),
(119, 'Lipa', 'Mains', 'January', 'Q1', '2021', 1638, 1689, 350, 188167, 17850, 10.54, 12712.77, 12.71),
(120, 'Lipa', 'Mains', 'February', 'Q1', '2021', 1656, 1707, 350, 156672, 17850, 8.78, 12712.77, 12.71),
(121, 'Lipa', 'Mains', 'March', 'Q1', '2021', 1745, 1796, 350, 313300, 17850, 17.55, 12712.77, 12.71),
(122, 'Lipa', 'Mains', 'April', 'Q2', '2021', 1793, 1845, 350, 228917, 18200, 12.58, 12962.04, 12.96),
(123, 'Lipa', 'Mains', 'May', 'Q2', '2021', 1812, 1862, 350, 241524, 17500, 13.8, 12463.5, 12.46),
(124, 'Lipa', 'Mains', 'June', 'Q2', '2021', 1875, 1925, 350, 247535, 17500, 14.14, 12463.5, 12.46),
(125, 'Lipa', 'Mains', 'July', 'Q3', '2021', 1949, 2000, 350, 183038, 17850, 10.25, 12712.77, 12.71),
(126, 'Lipa', 'Mains', 'August', 'Q3', '2021', 1968, 2019, 350, 233371, 17850, 13.07, 12712.77, 12.71),
(127, 'Lipa', 'Mains', 'September', 'Q3', '2021', 2012, 2063, 350, 160467, 17850, 8.99, 12712.77, 12.71),
(128, 'Lipa', 'Mains', 'October', 'Q4', '2021', 2062, 2114, 350, 151961, 18200, 8.35, 12962.04, 12.96),
(129, 'Lipa', 'Mains', 'November', 'Q4', '2021', 2133, 2185, 350, 238653, 18200, 13.11, 12962.04, 12.96),
(130, 'Lipa', 'Mains', 'December', 'Q4', '2021', 2169, 2220, 350, 155946, 17850, 8.74, 12712.77, 12.71),
(131, 'Lipa', 'Mains', 'January', 'Q1', '2020', 1004, 1056, 350, 174822, 18200, 9.61, 12962.04, 12.96),
(132, 'Lipa', 'Mains', 'February', 'Q1', '2020', 1052, 1102, 350, 212318, 17500, 12.13, 12463.5, 12.46),
(133, 'Lipa', 'Mains', 'March', 'Q1', '2020', 1128, 1179, 350, 161761, 17850, 9.06, 12712.77, 12.71),
(134, 'Lipa', 'Mains', 'April', 'Q2', '2020', 1157, 1208, 350, 245864, 17850, 13.77, 12712.77, 12.71),
(135, 'Lipa', 'Mains', 'May', 'Q2', '2020', 1208, 1279, 350, 230062, 24850, 9.26, 17698.17, 17.7),
(136, 'Lipa', 'Mains', 'June', 'Q2', '2020', 1279, 1316, 350, 182499, 12950, 14.09, 9222.99, 9.22),
(137, 'Lipa', 'Mains', 'July', 'Q3', '2020', 1316, 1387, 350, 143028, 24850, 5.76, 17698.17, 17.7),
(138, 'Lipa', 'Mains', 'August', 'Q3', '2020', 1387, 1439, 350, 155251, 18200, 8.53, 12962.04, 12.96),
(139, 'Lipa', 'Mains', 'September', 'Q3', '2020', 1439, 1459, 350, 186166, 7000, 26.6, 4985.4, 4.99),
(141, 'Lipa', 'Mains', 'October', 'Q4', '2020', 1459, 1542, 350, 157588, 29050, 5.42, 20689.41, 20.69),
(142, 'Lipa', 'Mains', 'November', 'Q4', '2020', 1542, 1575, 350, 171069, 11550, 14.81, 8225.91, 8.23),
(143, 'Lipa', 'Mains', 'December', 'Q4', '2020', 1575, 1638, 350, 165026, 22050, 7.48, 15704.01, 15.7),
(178, 'Lipa', 'Mains', 'January', 'Q1', '2024', 2022, 2059, 350, 12950, 37, 350, 26.35, 0.03),
(179, 'Lipa', 'Mains', 'February', 'Q1', '2024', 2059, 2119, 350, 21000, 60, 350, 42.73, 0.04),
(180, 'Lipa', 'Mains', 'March', 'Q1', '2024', 2119, 2169, 350, 17500, 50, 350, 35.61, 0.04),
(181, 'Lipa', 'Mains', 'April', 'Q2', '2024', 2169, 2228, 350, 20650, 59, 350, 42.02, 0.04),
(182, 'Lipa', 'Mains', 'May', 'Q2', '2024', 2228, 2294, 350, 23100, 66, 350, 47.01, 0.05),
(183, 'Lipa', 'Mains', 'June', 'Q2', '2024', 2294, 2328, 350, 11900, 34, 350, 24.21, 0.02),
(184, 'Lobo', 'Solar', 'January', 'Q1', '2021', 67, 68, 1, 345, 1, 345, 0.71, 0),
(185, 'Lipa', 'Solar', 'January', 'Q1', '2021', 100, 200, 1000, 100, 100000, 0, 71220, 71.22),
(186, 'Lipa', 'Solar', 'February', 'Q1', '2021', 100, 150, 5000, 4000, 250000, 0.02, 178050, 178.05),
(187, 'Lipa', 'Mains', 'July', 'Q3', '2024', 2500, 2800, 300, 3400, 90000, 0.04, 64098, 64.1),
(188, 'Lipa', 'Mains', 'August', 'Q3', '2024', 2800, 2900, 100, 200, 10000, 0.02, 7122, 7.12),
(189, 'Lipa', 'Mains', 'September', 'Q3', '2024', 700, 800, 100, 700, 10000, 0.07, 7122, 7.12),
(190, 'Lipa', 'Mains', 'October', 'Q4', '2024', 890, 900, 10, 5600, 100, 56, 71.22, 0.07),
(191, 'Lipa', 'Mains', 'January', 'Q1', '2019', 902, 925, 23, 2300, 23, 100, 16.38, 0.02),
(192, 'Lipa', 'Mains', 'February', 'Q1', '2019', 925, 963, 38, 1400, 38, 36.84, 27.06, 0.03),
(193, 'Lipa', 'Mains', 'March', 'Q1', '2019', 963, 975, 12, 500, 12, 41.67, 8.55, 0.01),
(194, 'Lipa', 'Mains', 'April', 'Q2', '2019', 975, 997, 22, 890, 22, 40.45, 15.67, 0.02),
(195, 'Lipa', 'Mains', 'May', 'Q2', '2019', 997, 1045, 48, 4212, 48, 87.75, 34.19, 0.03),
(196, 'Lipa', 'Mains', 'June', 'Q2', '2019', 1045, 1085, 40, 1390, 40, 34.75, 28.49, 0.03),
(197, 'Lipa', 'Mains', 'July', 'Q3', '2019', 1085, 1111, 26, 2390, 26, 91.92, 18.52, 0.02),
(198, 'Lipa', 'Mains', 'August', 'Q3', '2019', 1111, 1158, 47, 4500, 47, 95.74, 33.47, 0.03),
(199, 'Lipa', 'Mains', 'September', 'Q3', '2019', 1158, 1193, 35, 3400, 35, 97.14, 24.93, 0.02),
(200, 'Lipa', 'Solar', 'October', 'Q4', '2019', 1193, 1214, 21, 4000, 21, 190.48, 14.96, 0.01),
(201, 'Lipa', 'Mains', 'November', 'Q4', '2019', 1214, 1235, 21, 670, 21, 31.9, 14.96, 0.01),
(202, 'Lipa', 'Mains', 'December', 'Q4', '2019', 1235, 1269, 34, 1200, 34, 35.29, 24.21, 0.02);

-- --------------------------------------------------------

--
-- Table structure for table `fuel_emissions`
--

CREATE TABLE `fuel_emissions` (
  `id` int(11) NOT NULL,
  `campus` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `driver` varchar(255) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `vehicle_equipment` varchar(255) DEFAULT NULL,
  `plate_no` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `item_description` varchar(255) DEFAULT NULL,
  `transaction_no` varchar(50) DEFAULT NULL,
  `odometer` int(11) DEFAULT NULL,
  `quantity_liters` float(5,2) DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `co2_emission` float DEFAULT NULL,
  `nh4_emission` float DEFAULT NULL,
  `n2o_emission` float DEFAULT NULL,
  `total_emission` float DEFAULT NULL,
  `total_emission_t` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fuel_emissions`
--

INSERT INTO `fuel_emissions` (`id`, `campus`, `date`, `driver`, `type`, `vehicle_equipment`, `plate_no`, `category`, `fuel_type`, `item_description`, `transaction_no`, `odometer`, `quantity_liters`, `total_amount`, `co2_emission`, `nh4_emission`, `n2o_emission`, `total_emission`, `total_emission_t`) VALUES
(202, 'Lipa', '2024-01-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0001', 1750, 205.00, 11955.1, 523.98, 0.56, 9.22, 533.77, 0.534),
(204, 'Lipa', '2024-02-28', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0002', 1768, 199.00, 11845.2, 508.64, 0.55, 8.95, 518.15, 0.518),
(205, 'Lipa', '2024-03-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0003', 1810, 220.00, 11998.9, 562.32, 0.6, 9.9, 572.82, 0.573),
(206, 'Lipa', '2024-04-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0004', 173, 191.00, 11537.6, 488.2, 0.53, 8.59, 497.32, 0.497),
(207, 'Lipa', '2024-05-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0005', 1982, 148.00, 8611.13, 378.29, 0.41, 6.66, 385.35, 0.385),
(208, 'Lipa', '2024-06-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0006', 1705, 182.00, 10513.9, 465.19, 0.5, 8.19, 473.88, 0.474),
(210, 'Lipa', '2023-01-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0001', 849, 91.75, 5372, 234.51, 0.25, 4.13, 238.89, 0.239),
(211, 'Lipa', '2024-02-28', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0002', 926, 53.41, 3204.6, 136.52, 0.15, 2.4, 139.07, 0.139),
(212, 'Lipa', '2024-03-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0003', 1149, 149.60, 8579.56, 382.38, 0.41, 6.73, 389.52, 0.39),
(213, 'Lipa', '2023-04-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0004', 1137, 134.79, 7658.77, 344.52, 0.37, 6.07, 350.96, 0.351),
(214, 'Lipa', '2023-05-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0005', 2008, 124.55, 6635.34, 318.35, 0.34, 5.6, 324.3, 0.324),
(215, 'Lipa', '2024-06-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0006', 1204, 143.69, 7710.41, 367.27, 0.4, 6.47, 374.13, 0.374),
(216, 'Lipa', '2023-07-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0007', 2187, 186.06, 10311.5, 475.57, 0.51, 8.37, 484.45, 0.484),
(217, 'Lipa', '2023-08-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0008', 1606, 193.97, 11996.3, 495.79, 0.53, 8.73, 505.05, 0.505),
(218, 'Lipa', '2023-09-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0009', 2628, 230.30, 15331.7, 588.65, 0.63, 10.36, 599.64, 0.6),
(219, 'Lipa', '2023-10-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0011', 2446, 200.30, 12911.3, 511.97, 0.55, 9.01, 521.53, 0.522),
(220, 'Lipa', '2023-11-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0011', 2904, 208.36, 12539.1, 532.57, 0.57, 9.38, 542.52, 0.543),
(221, 'Lipa', '2023-12-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0012', 1333, 224.22, 12274.7, 573.11, 0.62, 10.09, 583.81, 0.584),
(222, 'Lipa', '2022-01-31', 'Ana M.', 'Vehicle', 'Toyota Grandia', 'D5N156', 'fuel', 'Diesel', 'DKD', '0001', 1682, 122.49, 6803.09, 313.08, 0.34, 5.51, 318.93, 0.319),
(223, 'Lipa', '2023-02-28', 'Ana M.', 'Vehicle', 'Toyota Hilux', 'K5K142', 'fuel', 'Diesel', 'Diesel Max', '0002', 1305, 163.50, 8250.21, 417.91, 0.45, 7.36, 425.71, 0.426),
(224, 'Lipa', '2022-03-31', 'John D.', 'Vehicle', 'Nissan Urvan', 'AS8125', 'fuel', 'Diesel', 'Diesel Max', '0003', 1136, 124.06, 7769.88, 317.1, 0.34, 5.58, 323.02, 0.323),
(225, 'Lipa', '2022-04-30', 'Roman L.', 'Vehicle', 'Hyundai Starex', 'E4D478', 'fuel', 'Diesel', 'Diesel Max', '0004', 1730, 112.45, 7761.3, 287.42, 0.31, 5.06, 292.79, 0.293),
(226, 'Lipa', '2022-05-31', 'Ana M.', 'Vehicle', 'Mitsubishi L300 FB Van', 'A6S125', 'fuel', 'Diesel', 'Diesel Max', '0005', 1407, 123.30, 6563.65, 315.15, 0.34, 5.55, 321.04, 0.321),
(227, 'Lipa', '2022-06-30', 'Roman L.', 'Vehicle', 'Isuzu Traviz', 'A1S521', 'fuel', 'Diesel', 'Diesel Max', '0006', 1597, 63.76, 3634.96, 162.97, 0.18, 2.87, 166.01, 0.166),
(228, 'Lipa', '2022-07-31', 'Maria S.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0007', 1307, 81.47, 5157.05, 208.24, 0.22, 3.67, 212.13, 0.212),
(229, 'Lipa', '2022-08-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0008', 1158, 56.85, 3948.23, 145.31, 0.16, 2.56, 148.02, 0.148),
(230, 'Lipa', '2022-09-30', 'Maria S.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0009', 1931, 78.87, 5496.45, 201.59, 0.22, 3.55, 205.36, 0.205),
(231, 'Lipa', '2022-10-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0010', 1347, 131.03, 6893.49, 334.91, 0.36, 5.9, 341.17, 0.341),
(232, 'Lipa', '2022-11-30', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0011', 1013, 131.10, 8008.9, 335.09, 0.36, 5.9, 341.35, 0.341),
(233, 'Lipa', '2022-12-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0012', 1755, 142.91, 9583.54, 365.28, 0.39, 6.43, 372.1, 0.372),
(234, 'Lipa', '2021-01-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0001', 1298, 137.27, 7227.27, 350.86, 0.38, 6.18, 357.42, 0.357),
(235, 'Lipa', '2021-02-28', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0002', 1375, 150.79, 9655.08, 385.42, 0.41, 6.79, 392.62, 0.393),
(237, 'Lipa', '2021-03-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0003', 1380, 147.18, 9755.09, 376.19, 0.4, 6.62, 383.22, 0.383),
(239, 'Lipa', '2021-05-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0005', 1369, 99.81, 6689.88, 255.11, 0.27, 4.49, 259.88, 0.26),
(240, 'Lipa', '2021-06-30', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0006', 1067, 138.35, 8656.56, 353.62, 0.38, 6.23, 360.23, 0.36),
(241, 'Lipa', '2021-07-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0007', 1407, 171.80, 9909.42, 439.12, 0.47, 7.73, 447.32, 0.447),
(242, 'Lipa', '2021-08-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0008', 1801, 167.14, 9483.52, 427.21, 0.46, 7.52, 435.19, 0.435),
(243, 'Lipa', '2021-09-30', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0009', 1802, 80.02, 4293.07, 204.53, 0.22, 3.6, 208.35, 0.208),
(244, 'Lipa', '2021-10-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0010', 1925, 154.03, 9893.35, 393.7, 0.42, 6.93, 401.06, 0.401),
(245, 'Lipa', '2021-11-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0010', 1173, 90.50, 4964.83, 231.32, 0.25, 4.07, 235.64, 0.236),
(246, 'Lipa', '2021-12-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0011', 1173, 154.03, 4964.83, 393.7, 0.42, 6.93, 401.06, 0.401),
(247, 'Lipa', '2020-01-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0001', 1481, 97.98, 5947.39, 250.44, 0.27, 4.41, 255.12, 0.255),
(248, 'Lipa', '2020-02-29', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0002', 1479, 108.51, 5959.93, 277.35, 0.3, 4.88, 282.53, 0.283),
(249, 'Lipa', '2020-03-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0003', 1625, 100.79, 5140.29, 257.62, 0.28, 4.54, 262.43, 0.262),
(250, 'Lipa', '2020-04-30', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0004', 1454, 124.08, 7521.73, 317.15, 0.34, 5.58, 323.07, 0.323),
(251, 'Lipa', '2020-05-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0005', 1292, 106.61, 6617.28, 272.5, 0.29, 4.8, 277.59, 0.278),
(252, 'Lipa', '2020-06-30', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0006', 1605, 150.28, 9087.43, 384.12, 0.41, 6.76, 391.29, 0.391),
(253, 'Lipa', '2020-07-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0007', 1050, 126.73, 7202.07, 323.92, 0.35, 5.7, 329.97, 0.33),
(254, 'Lipa', '2020-08-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0008', 1776, 107.44, 5512.75, 274.62, 0.3, 4.83, 279.75, 0.28),
(255, 'Lipa', '2020-09-30', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0009', 1811, 68.18, 4538.74, 174.27, 0.19, 3.07, 177.52, 0.178),
(256, 'Lipa', '2020-10-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0010', 1664, 124.92, 6988.02, 319.3, 0.34, 5.62, 325.26, 0.325),
(257, 'Lipa', '2020-11-30', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0011', 1909, 137.16, 7794.8, 350.58, 0.38, 6.17, 357.13, 0.357),
(258, 'Lipa', '2020-12-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0012', 1048, 53.84, 3563.13, 137.62, 0.15, 2.42, 140.19, 0.14),
(259, 'Lipa', '2024-09-29', 'Lester', 'Vehicle', 'Toyota Hilux', '542', 'fuel', 'Diesel', 'gas', '541325642132', 89, 120.00, 344, 306.72, 0.33, 5.4, 312.45, 0.312),
(263, 'Lipa', '2024-08-30', 'Lester', 'Vehicle', 'Toyota Minibus', '542', 'fuel', 'Diesel', 'gas', '541325642132', 67, 43.00, 434, 109.91, 0.12, 1.93, 111.96, 0.112),
(264, 'Lipa', '2024-07-31', 'Lester', 'Vehicle', 'Toyota Hi-Ace', '542', 'fuel', 'Diesel', 'gas', '541325642132', 78, 88.00, 500, 224.93, 0.24, 3.96, 229.13, 0.229),
(265, 'Lipa', '2024-10-30', 'Lester', 'Vehicle', 'Toyota Hi-Ace', '542', 'fuel', 'Diesel', 'gas', '541325642132', 45, 78.00, 890, 199.37, 0.21, 3.51, 203.09, 0.203),
(270, 'Lipa', '2024-11-16', 'Lester', 'Vehicle', 'Toyota Hi-Ace', 'DAJ212', 'fuel', 'Diesel', 'gas', '12485', 4512, 45.25, 80, 115.66, 0.12, 2.04, 117.82, 0.118),
(271, 'Lipa', '2024-12-16', 'cere', 'Vehicle', 'Toyota Grandia', 'ads123', 'fuel', 'Diesel', 'gas', '12485', 125, 25.36, 98, 64.81, 0.07, 1.14, 66.02, 0.066),
(272, 'Lipa', '2025-01-16', 'Dianne', 'Vehicle', 'Toyota Grandia', 'AJKH542', 'fuel', 'Diesel', 'Diesel Max', '00124', 5482, 12.36, 105, 31.59, 0.03, 0.56, 32.18, 0.032);

-- --------------------------------------------------------

--
-- Table structure for table `tblaccommodation`
--

CREATE TABLE `tblaccommodation` (
  `id` int(11) NOT NULL,
  `Campus` varchar(255) NOT NULL,
  `Office` varchar(255) DEFAULT NULL,
  `YearTransact` year(4) NOT NULL,
  `TravellerName` varchar(255) DEFAULT NULL,
  `TravelPurpose` varchar(255) DEFAULT NULL,
  `TravelDateFrom` date DEFAULT NULL,
  `TravelDateTo` date DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `TravelType` varchar(255) DEFAULT NULL,
  `NumOccupiedRoom` int(11) DEFAULT NULL,
  `NumNightPerRoom` int(11) DEFAULT NULL,
  `Factor` decimal(10,2) DEFAULT NULL,
  `GHGEmissionKGC02e` decimal(10,2) DEFAULT NULL,
  `GHGEmissionTC02e` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblaccommodation`
--

INSERT INTO `tblaccommodation` (`id`, `Campus`, `Office`, `YearTransact`, `TravellerName`, `TravelPurpose`, `TravelDateFrom`, `TravelDateTo`, `Country`, `TravelType`, `NumOccupiedRoom`, `NumNightPerRoom`, `Factor`, `GHGEmissionKGC02e`, `GHGEmissionTC02e`) VALUES
(78, 'Lipa', 'OVCDEA', '2020', 'Dianne Castillo', 'Conference', '2020-01-10', '2020-01-13', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(79, 'Lipa', 'OVCDEA', '2020', 'Kyla Pusag', 'Meetings', '2020-02-11', '2020-02-12', 'China', 'International', 1, 3, 76.74, 230.22, 0.23),
(80, 'Lipa', 'RGO', '2020', 'Lester Cuya', 'Conference', '2020-03-24', '2020-03-26', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(81, 'Lipa', 'OVCDEA', '2020', 'Lester Cuya', 'Conference', '2020-04-22', '2020-04-26', 'Cambodia', 'International', 2, 3, 16.77, 100.62, 0.10),
(82, 'Lipa', 'RGO', '2020', 'Dianne Castillo', 'Meetings', '2020-05-24', '2020-05-28', 'Hong Kong', 'International', 1, 4, 56.63, 226.52, 0.23),
(83, 'Lipa', 'RGO', '2020', 'Kyla Pusag', 'Conference', '2020-06-10', '2020-06-12', 'Singapore', 'International', 2, 2, 51.33, 205.32, 0.21),
(84, 'Lipa', 'RGO', '2020', 'Dianne Castillo', 'Meetings', '2020-07-01', '2020-07-04', 'Australia', 'International', 1, 3, 51.47, 154.41, 0.15),
(85, 'Lipa', 'OVCDEA', '2020', 'Lester Cuya', 'Conference', '2020-08-04', '2020-08-05', 'Philippines', 'Local', 1, 1, 66.54, 66.54, 0.07),
(86, 'Lipa', 'OVCDEA', '2020', 'Dianne Castillo', 'Meeting Conference ', '2020-09-28', '2020-09-30', 'Singapore', 'International', 1, 2, 51.33, 102.66, 0.10),
(87, 'Lipa', 'RGO', '2020', 'Kyla Pusag', 'Conference', '2020-10-14', '2020-10-17', 'Philippines', 'Local', 1, 3, 66.54, 199.62, 0.20),
(88, 'Lipa', 'OVCDEA', '2020', 'Lester Cuya', 'Conference', '2020-11-15', '2020-11-18', 'Japan', 'International', 1, 3, 81.86, 245.58, 0.25),
(89, 'Lipa', 'RGO', '2020', 'Dianne Castillo', 'Conference', '2020-12-15', '2020-12-18', 'Japan', 'International', 1, 3, 81.86, 245.58, 0.25),
(90, 'Lipa', 'RGO', '2021', 'Dianne Castillo', 'Awarding', '2021-01-27', '2021-01-28', 'Hong Kong', 'International', 1, 1, 56.63, 56.63, 0.06),
(91, 'Lipa', 'OVCDEA', '2021', 'Kyla Pusag', 'Awarding', '2021-02-09', '2021-02-11', 'Philippines', 'Local', 1, 1, 66.54, 66.54, 0.07),
(92, 'Lipa', 'OVCDEA', '2021', 'Lester Cuya', 'Conference', '2021-03-24', '2021-03-26', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(93, 'Lipa', 'RGO', '2021', 'Lester Cuya', 'Meeting Conference ', '2021-04-04', '2021-04-09', 'Taiwan', 'Local', 1, 5, 10.75, 53.75, 0.05),
(94, 'Lipa', 'OVCDEA', '2021', 'Kyla Pusag', 'Meetings', '2021-05-19', '2021-05-21', 'New Zealand', 'International', 2, 2, 11.57, 46.28, 0.05),
(95, 'Lipa', 'OVCDEA', '2021', 'Lester Cuya', 'Conference', '2021-06-16', '2021-06-20', 'China', 'International', 2, 4, 76.74, 613.92, 0.61),
(96, 'Lipa', 'OVCDEA', '2021', 'Lester Cuya', 'Conference', '2021-07-01', '2021-07-02', 'Philippines', 'Local', 4, 1, 66.54, 266.16, 0.27),
(97, 'Lipa', 'OVCDEA', '2021', 'Dianne Castillo', 'Conference', '2021-08-30', '2021-08-31', 'Philippines', 'Local', 3, 1, 66.54, 199.62, 0.20),
(98, 'Lipa', 'OVCDEA', '2021', 'Dianne Castillo', 'Conference', '2021-09-15', '2021-09-18', 'Brazil', 'International', 3, 2, 16.77, 100.62, 0.10),
(99, 'Lipa', 'OVCDEA', '2021', 'Lester Cuya', 'Conference', '2021-11-25', '2021-10-28', 'Switzerland', 'International', 4, 3, 10.75, 129.00, 0.13),
(100, 'Lipa', 'OVCDEA', '2021', 'Kyla', 'Meeting Conference ', '2021-12-01', '2021-12-04', 'Thailand', 'International', 2, 3, 59.05, 354.30, 0.35),
(101, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Conference', '2022-01-03', '2022-01-09', 'Macau', 'International', 1, 6, 85.19, 511.14, 0.51),
(102, 'Lipa', 'OVCDEA', '2022', 'Lester Cuya', 'Conference', '2022-02-10', '2021-02-12', 'Brunei', 'International', 1, 2, 16.77, 33.54, 0.03),
(103, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Conference', '2022-03-23', '2022-03-25', 'Belize', 'International', 1, 3, 16.04, 48.12, 0.05),
(104, 'Lipa', 'OVCDEA', '2022', 'Lester Cuya', 'Meetings', '2022-04-19', '2022-04-22', 'Chile', 'International', 3, 3, 38.50, 346.50, 0.35),
(105, 'Lipa', 'RGO', '2022', 'Lester Cuya', 'Conference', '2022-05-19', '2022-05-24', 'Greece', 'International', 2, 5, 56.63, 566.30, 0.57),
(106, 'Lipa', 'OVCDEA', '2022', 'Kyla Pusag', 'Conference', '2022-06-23', '2022-06-26', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(107, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Meeting Conference ', '2022-07-14', '2022-07-20', 'Singapore', 'International', 2, 6, 51.33, 615.96, 0.62),
(108, 'Lipa', 'RGO', '2022', 'Dianne Castillo', 'Meeting Conference ', '2022-08-17', '2022-08-19', 'Singapore', 'International', 2, 2, 51.33, 205.32, 0.21),
(109, 'Lipa', 'OVCDEA', '2022', 'Lester Cuya', 'Conference', '2022-09-19', '2022-09-20', 'Taiwan', 'International', 1, 1, 10.75, 10.75, 0.01),
(110, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Conference', '2022-10-01', '2022-10-03', 'Singapore', 'International', 2, 3, 51.33, 307.98, 0.31),
(111, 'Lipa', 'RGO', '2022', 'Lester Cuya', 'Meetings', '2022-11-02', '2022-11-04', 'Hong Kong', 'International', 2, 3, 56.63, 339.78, 0.34),
(112, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Conference', '2022-12-01', '2022-12-09', 'Singapore', 'International', 1, 9, 51.33, 461.97, 0.46),
(113, 'Lipa', 'RGO', '2023', 'Richelle Sulit', 'Conference', '2023-01-03', '2023-01-09', 'Philippines', 'Local', 2, 7, 66.54, 931.56, 0.93),
(114, 'Lipa', 'OVCDEA', '2023', 'Kyla Pusag', 'Conference', '2023-02-02', '2023-02-01', 'Philippines', 'Local', 5, 1, 66.54, 332.70, 0.33),
(115, 'Lipa', 'OVCDEA', '2023', 'Lester Cuya', 'Conference', '2023-03-15', '2023-03-18', 'Indonesia', 'International', 2, 3, 110.37, 662.22, 0.66),
(116, 'Lipa', 'OVCDEA', '2023', 'Dianne Castillo', 'Meeting Conference ', '2023-04-20', '2023-04-24', 'Germany', 'International', 3, 3, 22.57, 203.13, 0.20),
(117, 'Lipa', 'OVCDEA', '2023', 'Kyla Pusag', 'Meeting Conference ', '2023-05-24', '2023-05-28', 'Japan', 'International', 2, 3, 81.86, 491.16, 0.49),
(118, 'Lipa', 'OVCDEA', '2023', 'Dianne Castillo', 'Conference', '2023-06-14', '2023-06-18', 'Brunei', 'International', 2, 5, 16.77, 167.70, 0.17),
(119, 'Lipa', 'OVCDEA', '2023', 'Lester Cuya', 'Meetings', '2023-06-21', '2023-06-23', 'France', 'International', 1, 2, 8.01, 16.02, 0.02),
(120, 'Lipa', 'RGO', '2023', 'Kyla Pusag', 'Meetings', '2023-07-18', '2023-07-20', 'Philippines', 'International', 3, 2, 66.54, 399.24, 0.40),
(121, 'Lipa', 'RGO', '2023', 'Dianne Castillo', 'Meetings', '2023-08-17', '2023-08-25', 'Hong Kong', 'International', 2, 9, 56.63, 1019.34, 1.02),
(122, 'Lipa', 'RGO', '2023', 'Lester Cuya', 'Conference', '2023-09-21', '2023-09-29', 'Hong Kong', 'International', 3, 9, 56.63, 1529.01, 1.53),
(123, 'Lipa', 'RGO', '2023', 'Kyla Pusag', 'Meetings', '2023-10-18', '2023-10-20', 'China', 'International', 2, 2, 76.74, 306.96, 0.31),
(124, 'Lipa', 'OVCDEA', '2023', 'Lester Cuya', 'Conference', '2023-11-24', '2023-11-28', 'South Korea', 'International', 1, 5, 82.36, 411.80, 0.41),
(125, 'Lipa', 'OVCDEA', '2023', 'Lester Cuya', 'Awarding', '2023-12-05', '2023-12-06', 'Philippines', 'Local', 2, 1, 66.54, 133.08, 0.13),
(126, 'Lipa', 'OVCDEA', '2024', 'Kyla Pusag', 'Conference', '2024-01-10', '2024-01-12', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(127, 'Lipa', 'OVCDEA', '2024', 'Lester Cuya', 'Meetings', '2024-02-15', '2024-02-17', 'Thailand', 'International', 1, 2, 59.05, 118.10, 0.12),
(128, 'Lipa', 'OVCDEA', '2024', 'Lester Cuya', 'Meetings', '2024-03-06', '2024-03-10', 'Singapore', 'International', 2, 4, 51.33, 410.64, 0.41),
(129, 'Lipa', 'OVCDEA', '2024', 'Dianne Castillo', 'Meeting Conference ', '2024-04-17', '2024-04-22', 'China', 'International', 3, 5, 76.74, 1151.10, 1.15),
(130, 'Lipa', 'OVCDEA', '2024', 'Kyla Pusag', 'Meeting Conference ', '2024-05-23', '2024-05-28', 'Japan', 'International', 3, 5, 81.86, 1227.90, 1.23),
(131, 'Lipa', 'OVCDEA', '2024', 'Dianne Castillo', 'Meetings', '2024-06-09', '2024-06-11', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(132, 'Lipa', 'OVCDEA', '2019', 'Dianne Castillo', 'Meetings', '2019-01-17', '2019-01-20', 'Austria', 'International', 2, 2, 18.73, 74.92, 0.07),
(133, 'Lipa', 'OVCDEA', '2019', 'Lester Cuya', 'Seminar', '2019-02-06', '2019-02-07', 'Philippines', 'Local', 3, 1, 66.54, 199.62, 0.20),
(134, 'Lipa', 'OVCDEA', '2019', 'Kyla Pusag', 'Conference', '2019-03-21', '2019-03-23', 'Japan', 'International', 2, 2, 81.86, 327.44, 0.33),
(135, 'Lipa', 'OVCDEA', '2019', 'Lester Cuya', 'Seminar', '2019-04-24', '2019-04-26', 'Cambodia', 'International', 3, 2, 16.77, 100.62, 0.10),
(136, 'Lipa', 'OVCDEA', '2019', 'Lester Cuya', 'Seminar', '2019-05-14', '2019-05-20', 'Taiwan', 'International', 1, 7, 10.75, 75.25, 0.08),
(137, 'Lipa', 'RGO', '2019', 'Lester Cuya', 'Seminar', '2019-06-18', '2019-06-20', 'China', 'International', 1, 2, 76.74, 153.48, 0.15),
(138, 'Lipa', 'OVCDEA', '2019', 'Kyla Pusag', 'Meeting Conference ', '2019-07-24', '2019-07-28', 'New Zealand', 'International', 2, 4, 11.57, 92.56, 0.09),
(139, 'Lipa', 'OVCDEA', '2019', 'Kyla Pusag', 'Meeting Conference ', '2019-08-20', '2019-08-22', 'Philippines', 'Local', 2, 4, 66.54, 532.32, 0.53),
(140, 'Lipa', 'RGO', '2019', 'Kyla Pusag', 'Meeting Conference ', '2019-09-17', '2019-09-20', 'Philippines', 'Local', 2, 3, 66.54, 399.24, 0.40),
(141, 'Lipa', 'OVCDEA', '2019', 'Lester Cuya', 'Seminar', '2019-10-23', '2019-10-25', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(142, 'Lipa', 'RGO', '2019', 'Dianne Castillo', 'Meetings', '2019-11-21', '2019-11-25', 'Japan', 'International', 2, 4, 81.86, 654.88, 0.65),
(143, 'Lipa', 'OVCDEA', '2019', 'Dianne Castillo', 'Meetings', '2019-12-03', '2019-12-04', 'Philippines', 'Local', 2, 1, 66.54, 133.08, 0.13);

-- --------------------------------------------------------

--
-- Table structure for table `tblflight`
--

CREATE TABLE `tblflight` (
  `ID` int(11) NOT NULL,
  `Campus` varchar(255) DEFAULT NULL,
  `Office` char(20) DEFAULT NULL,
  `Year` year(4) DEFAULT NULL,
  `TravellerName` varchar(30) DEFAULT NULL,
  `TravelPurpose` varchar(30) DEFAULT NULL,
  `TravelDate` date DEFAULT NULL,
  `DomesticInternational` varchar(30) DEFAULT NULL,
  `Origin` varchar(30) DEFAULT NULL,
  `Destination` varchar(30) DEFAULT NULL,
  `Class` varchar(30) DEFAULT NULL,
  `OnewayRoundTrip` varchar(30) DEFAULT NULL,
  `GHGEmissionKGC02e` float DEFAULT NULL,
  `GHGEmissionTC02e` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblflight`
--

INSERT INTO `tblflight` (`ID`, `Campus`, `Office`, `Year`, `TravellerName`, `TravelPurpose`, `TravelDate`, `DomesticInternational`, `Origin`, `Destination`, `Class`, `OnewayRoundTrip`, `GHGEmissionKGC02e`, `GHGEmissionTC02e`) VALUES
(13, 'Lipa', 'GSO', '2020', 'Dianne Castillo', 'Conference', '2020-01-13', 'International', 'MANILA', 'THAILAND', 'Economy', 'Round Trip', 964, 0.96),
(14, 'Lipa', 'OVCRDES', '2020', 'Lester Cuya', 'Conference', '2020-02-20', 'Domestic', 'MANILA', 'BACOLOD', 'Business Class', 'One Way', 381, 0.38),
(15, 'Lipa', 'OC', '2020', 'Kyla Pusag', 'Meeting', '2020-03-18', 'Domestic', 'MANILA', 'DAVAO', 'Economy', 'One Way', 165, 0.17),
(16, 'Lipa', 'OVCRDES', '2020', 'Dianne Castillo', 'Seminar', '2020-04-17', 'International', 'MANILA', 'OSAKA', 'Economy', 'Round Trip', 740, 0.74),
(17, 'Lipa', 'OC', '2020', 'Dianne Castillo', 'Seminar', '2020-05-10', 'Domestic', 'MANILA', 'ILOILO', 'Business Class', 'One Way', 279, 0.28),
(18, 'Lipa', 'RGO', '2020', 'Lester Cuya', 'Seminar', '2020-06-18', 'International', 'MANILA', 'SINGAPORE', 'Economy', 'Round Trip', 900, 0.9),
(19, 'Lipa', 'OVCRDES', '2020', 'Lester Cuya', 'Conference', '2020-07-08', 'Domestic', 'MANILA', 'PUERTO PRINCESA', 'Economy', 'One Way', 186, 0.19),
(20, 'Lipa', 'GSO', '2020', 'Lester Cuya', 'Conference', '2020-08-20', 'International', 'MANILA', 'CANADA', 'Economy', 'Round Trip', 5370, 5.37),
(21, 'Lipa', 'OC', '2020', 'Lester Cuya', 'Conference', '2020-09-27', 'Domestic', 'MANILA', 'ROXAS CITY', 'Economy', 'One Way', 174, 0.17),
(22, 'Lipa', 'RGO', '2020', 'Lester Cuya', 'Meeting', '2020-10-20', 'Domestic', 'MANILA', 'TAGBILARAN', 'Economy', 'One Way', 66, 0.07),
(23, 'Lipa', 'OVCRDES', '2020', 'Dianne Castillo', 'Meeting', '2020-11-26', 'International', 'MANILA', 'JAPAN', 'Economy', 'Round Trip', 2056, 2.06),
(24, 'Lipa', 'RGO', '2020', 'Kyla Pusag', 'Meeting', '2020-12-01', 'Domestic', 'MANILA', 'ANTIQUE', 'Economy', 'One Way', 183, 0.18),
(25, 'Lipa', 'OC', '2020', 'Kyla Pusag', 'Meeting', '2020-01-09', 'Domestic', 'MANILA', 'BUTUAN', 'Economy', 'Round Trip', 390, 0.39),
(26, 'Lipa', 'OC', '2021', 'Kyla Pusag', 'Meeting', '2021-01-14', 'International', 'MANILA', 'TAIWAN', 'Business Class', 'Round Trip', 1885, 1.89),
(27, 'Lipa', 'CICS', '2021', 'Dianne Castillo', 'Awarding', '2021-02-18', 'Domestic', 'MANILA', 'CEBU', 'Business Class', 'One Way', 375, 0.38),
(28, 'Lipa', 'GSO', '2021', 'Dianne Castillo', 'Awarding', '2021-03-25', 'Domestic', 'MANILA', 'CEBU', 'Economy', 'Round Trip', 234, 0.23),
(29, 'Lipa', 'GSO', '2021', 'Lester Cuya', 'Meeting', '2021-04-10', 'International', 'MANILA', 'COTOBATO', 'Economy', 'One Way', 260, 0.26),
(30, 'Lipa', 'CICS', '2021', 'Lester Cuya', 'Seminar', '2021-05-12', 'Domestic', 'MANILA', 'DIPOLOG', 'Business Class', 'One Way', 384, 0.38),
(31, 'Lipa', 'OVCRDES', '2021', 'Lester Cuya', 'Seminar', '2021-06-11', 'International', 'MANILA', 'CHINA', 'Business Class', 'Round Trip', 794, 0.79),
(32, 'Lipa', 'OC', '2021', 'Dianne Castillo', 'Seminar', '2021-07-22', 'Domestic', 'MANILA', 'SURIGAO', 'Business Class', 'One Way', 162, 0.16),
(33, 'Lipa', 'OVCRDES', '2021', 'Lester Cuya', 'Seminar', '2021-08-24', 'International', 'MANILA', 'SINGAPORE', 'Economy', 'One Way', 150, 0.15),
(34, 'Lipa', 'RGO', '2021', 'Lester Cuya', 'Seminar', '2021-09-07', 'International', 'MANILA', 'SINGAPORE', 'Economy', 'Round Trip', 1200, 1.2),
(35, 'Lipa', 'OC', '2021', 'Dianne Castillo', 'Conference', '2021-10-26', 'International', 'MANILA', 'SYDNEY', 'Business Class', 'Round Trip', 6552, 6.55),
(36, 'Lipa', 'CICS', '2021', 'Dianne Castillo', 'MEETING', '2021-11-17', 'Domestic', 'MANILA', 'TUGUEGARAO', 'Business Class', 'Round Trip', 326, 0.33),
(37, 'Lipa', 'OVCRDES', '2021', 'Dianne Castillo', 'Conference', '2021-12-07', 'Domestic', 'MANILA', 'CEBU', 'Economy', 'Round Trip', 352, 0.35),
(38, 'Lipa', 'RGO', '2022', 'Kyla Pusag', 'Seminar', '2022-01-19', 'Domestic', 'MANILA', 'BASCO', 'Economy', 'Round Trip', 306, 0.31),
(39, 'Lipa', 'RGO', '2022', 'Kyla Pusag', 'Conference', '2022-02-16', 'Domestic', 'MANILA', 'BACOLOD', 'Economy', 'Round Trip', 106, 0.11),
(40, 'Lipa', 'OVCRDES', '2022', 'Dianne Castillo', 'Conference', '2022-03-17', 'Domestic', 'MANILA', 'CAGAYAN DE ORO', 'Business Class', 'Round Trip', 268, 0.27),
(41, 'Lipa', 'OC', '2022', 'Lester Cuya', 'Meeting', '2022-04-20', 'International', 'MANILA', 'CHEJU', 'Economy', 'Round Trip', 768, 0.27),
(42, 'Lipa', 'RGO', '2022', 'Kyla Pusag', 'Meeting', '2022-05-18', 'International', 'MANILA', 'SINGAPORE', 'Business Class', 'One Way', 1404, 1.4),
(43, 'Lipa', 'OVCDEA', '2022', 'Dianne Castillo', 'Seminar', '2022-06-29', 'Domestic', 'MANILA', 'TACLOBAN', 'Business Class', 'One Way', 355, 0.36),
(44, 'Lipa', 'OVCRDES', '2022', 'Dianne Castillo', 'Conference', '2022-07-13', 'Domestic', 'MANILA', 'ROXAS CITY', 'Business Class', 'One Way', 250, 0.25),
(45, 'Lipa', 'OC', '2022', 'Lester Cuya', 'Conference', '2022-08-18', 'International', 'MANILA', 'SEA', 'Economy', 'Round Trip', 2716, 2.72),
(46, 'Lipa', 'RGO', '2022', 'Dianne Castillo', 'Seminar', '2022-09-16', 'Domestic', 'MANILA', 'ZAMBOANGA', 'Economy', 'One Way', 81, 0.08),
(47, 'Lipa', 'GSO', '2022', 'Dianne Castillo', 'Awarding', '2022-10-05', 'Domestic', 'MANILA', 'CEBU', 'Economy', 'Round Trip', 470, 0.47),
(48, 'Lipa', 'RGO', '2022', 'Lester Cuya', 'Awarding', '2022-11-16', 'International', 'MANILA', 'JAPAN', 'Business Class', 'Round Trip', 2238, 2.24),
(49, 'Lipa', 'ACCOUNTING', '2022', 'Kyla Pusag', 'Seminar', '2022-12-13', 'International', 'MANILA', 'KOREA', 'Business Class', 'Round Trip', 2512, 2.51),
(50, 'Lipa', 'OVCRDES', '2023', 'Lester Cuya', 'Seminar', '2023-01-04', 'International', 'MANILA', 'HONGKONG', 'Business Class', 'Round Trip', 1040, 1.04),
(51, 'Lipa', 'OVCRDES', '2023', 'Lester Cuya', 'Seminar', '2023-02-15', 'International', 'MANILA', 'HONGKONG', 'Business Class', 'One Way', 780, 0.78),
(52, 'Lipa', 'OVCRDES', '2023', 'Lester Cuya', 'Seminar', '2024-03-21', 'Domestic', 'MANILA', 'TACLOBAN', 'Business Class', 'One Way', 355, 0.36),
(53, 'Lipa', 'RGO', '2023', 'Kyla Pusag', 'Seminar', '2023-04-10', 'Domestic', 'MANILA', 'OSAMIS', 'Business Class', 'One Way', 406, 0.41),
(54, 'Lipa', 'OC', '2023', 'Kyla Pusag', 'Seminar', '2023-05-30', 'Domestic', 'MANILA', 'NAGA', 'Economy', 'One Way', 125, 0.13),
(55, 'Lipa', 'OVCRDES', '2023', 'Lester Cuya', 'Seminar', '2023-06-06', 'Domestic', 'MANILA', 'MASBATE', 'Business Class', 'One Way', 65, 0.07),
(56, 'Lipa', 'OVCDEA', '2023', 'Kyla Pusag', 'Seminar', '2023-07-14', 'International', 'MANILA', 'OMAN', 'Business Class', 'Round Trip', 6265, 6.27),
(57, 'Lipa', 'OVCRDES', '2023', 'Dianne Castillo', 'Seminar', '2023-08-08', 'International', 'MANILA', 'TAIWAN', 'Economy', 'Round Trip', 626, 0.63),
(58, 'Lipa', 'OC', '2023', 'Dianne Castillo', 'Meeting', '2023-09-05', 'Domestic', 'MANILA', 'TAGBILARAN', 'Economy', 'One Way', 131, 0.13),
(60, 'Lipa', 'OVCRDES', '2023', 'Dianne Castillo', 'Conference', '2023-10-19', 'International', 'MANILA', 'CAMBODIA', 'Economy', 'Round Trip', 568, 0.57),
(61, 'Lipa', 'CICS', '2023', 'Dianne Castillo', 'Seminar', '2023-11-23', 'Domestic', 'MANILA', 'SAN JOSE', 'Economy', 'One Way', 46, 0.05),
(62, 'Lipa', 'RGO', '2023', 'Kyla Pusag', 'Seminar', '2023-12-06', 'Domestic', 'MANILA', 'PAGADIAN', 'Business Class', 'One Way', 207, 0.21),
(63, 'Lipa', 'OVCDEA', '2024', 'Kyla Pusag', 'Seminar', '2024-01-17', 'International', 'MANILA', 'HONGKONG', 'Business Class', 'Round Trip', 1560, 1.56),
(64, 'Lipa', 'CICS', '2024', 'Dianne Castillo', 'Seminar', '2024-02-15', 'International', 'MANILA', 'SINGAPORE', 'Economy', 'Round Trip', 1200, 1.2),
(65, 'Lipa', 'OC', '2024', 'Lester Cuya', 'Seminar', '2024-03-29', 'International', 'MANILA', 'MACAU', 'Economy', 'Round Trip', 742, 0.74),
(66, 'Lipa', 'CICS', '2024', 'Lester Cuya', 'Conference', '2024-04-12', 'Domestic', 'MANILA', 'MASBATE', 'Economy', 'One Way', 130, 0.13),
(67, 'Lipa', 'OVCRDES', '2024', 'Lester Cuya', 'Conference', '2023-05-17', 'Domestic', 'MANILA', 'ILOILO', 'Business Class', 'Round Trip', 372, 0.37),
(68, 'Lipa', 'CICS', '2024', 'Lester Cuya', 'Conference', '2024-06-18', 'Domestic', 'MANILA', 'LAOAG', 'Economy', 'One Way', 102, 0.1),
(69, 'Lipa', 'CICS', '2019', 'Kyla Pusag', 'Conference', '2019-01-17', 'International', 'MANILA', 'CANADA', 'Economy', 'Round Trip', 3516, 3.52),
(70, 'Lipa', 'OVCRDES', '2019', 'Kyla Pusag', 'Conference', '2019-02-27', 'International', 'MANILA', 'CEBU', 'Business Class', 'Round Trip', 520, 0.52),
(71, 'Lipa', 'OVCRDES', '2019', 'Kyla Pusag', 'Conference', '2019-03-19', 'Domestic', 'MANILA', 'CEBU', 'Business Class', 'One Way', 6496, 0.65),
(72, 'Lipa', 'RGO', '2019', 'Kyla Pusag', 'Meeting', '2019-04-24', 'Domestic', 'MANILA', 'LAOAG', 'Business Class', 'Round Trip', 880, 0.88),
(73, 'Lipa', 'CICS', '2019', 'Kyla Pusag', 'Meeting', '2019-05-14', 'Domestic', 'MANILA', 'ILOILO', 'Business Class', 'Round Trip', 938, 0.94),
(74, 'Lipa', 'ACCOUNTING', '2019', 'Kyla Pusag', 'Meeting', '2019-06-23', 'Domestic', 'MANILA', 'MASBATE', 'Business Class', 'Round Trip', 326, 0.33),
(75, 'Lipa', 'GSO', '2019', 'Kyla Pusag', 'Meeting', '2019-07-24', 'Domestic', 'MANILA', 'CAGAYAN DE ORO', 'Economy', 'One Way', 323, 0.32),
(76, 'Lipa', 'OC', '2019', 'Kyla Pusag', 'Meeting', '2019-08-21', 'Domestic', 'MANILA', 'CEBU', 'Business Class', 'Round Trip', 804, 0.8),
(77, 'Lipa', 'RGO', '2019', 'Kyla Pusag', 'Meeting', '2019-09-25', 'Domestic', 'MANILA', 'DAVAO', 'Economy', 'One Way', 161, 0.16),
(78, 'Lipa', 'CICS', '2019', 'Kyla Pusag', 'Meeting', '2019-10-24', 'Domestic', 'MANILA', 'DIPOLOG', 'Business Class', 'One Way', 256, 0.26),
(79, 'Lipa', 'RGO', '2019', 'Dianne Castillo', 'Meeting', '2019-11-20', 'Domestic', 'MANILA', 'NAGA', 'Business Class', 'Round Trip', 150, 0.15),
(80, 'Lipa', 'RGO', '2019', 'Dianne Castillo', 'Meeting', '2019-12-10', 'Domestic', 'MANILA', 'TACLOBAN', 'Business Class', 'Round Trip', 226, 0.23),
(81, 'Lipa', 'RGO', '2024', 'Dianne Castillo', 'Meeting', '2024-07-24', 'Domestic', 'MANILA', 'TACLOBAN', 'Economy', 'One Way', 176, 0.18),
(82, 'Lipa', 'RGO', '2024', 'Dianne Castillo', 'Awarding', '2024-08-23', 'Domestic', 'MANILA', 'SINGAPORE', 'Economy', 'Round Trip', 914, 0.91),
(83, 'Lipa', 'OVCRDES', '2024', 'Dianne Castillo', 'Awarding', '2024-09-22', 'Domestic', 'MANILA', 'CEBU', 'Economy', 'One Way', 288, 0.29),
(84, 'Lipa', 'GSO', '2024', 'Dianne Castillo', 'Awarding', '2024-10-01', 'Domestic', 'MANILA', 'KALIBO', 'Economy', 'Round Trip', 232, 0.23);

-- --------------------------------------------------------

--
-- Table structure for table `tblfoodwaste`
--

CREATE TABLE `tblfoodwaste` (
  `id` int(11) NOT NULL,
  `Campus` varchar(255) DEFAULT NULL,
  `YearTransaction` varchar(4) DEFAULT NULL,
  `Month` varchar(20) DEFAULT NULL,
  `Office` varchar(255) DEFAULT NULL,
  `TypeOfFoodServed` varchar(255) DEFAULT NULL,
  `QuantityOfServing` double DEFAULT NULL,
  `GHGEmissionKGCO2e` double DEFAULT NULL,
  `GHGEmissionTCO2e` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblfoodwaste`
--

INSERT INTO `tblfoodwaste` (`id`, `Campus`, `YearTransaction`, `Month`, `Office`, `TypeOfFoodServed`, `QuantityOfServing`, `GHGEmissionKGCO2e`, `GHGEmissionTCO2e`) VALUES
(80, 'Lipa', '2020', 'January', 'Procurement', '1 Standard Breakfast', 10.9, 9.156, 0.009156000000000001),
(81, 'Lipa', '2020', 'February', 'Auxillary Services', '1 Hot Snack (burger and fries)', 15.9, 44.043, 0.044043),
(82, 'Lipa', '2020', 'March', 'Auxillary Services', '1 Average Meal', 20.6, 96.82000000000001, 0.09682),
(83, 'Lipa', '2020', 'April', 'Auxillary Services', 'Meal,Vegetarian', 13.4, 38.190000000000005, 0.03819),
(84, 'Lipa', '2020', 'May', 'Procurement', '1 Sandwich', 20.3, 25.781000000000002, 0.025781000000000002),
(85, 'Lipa', '2020', 'June', 'Auxillary Services', '1 Hot Snack (burger and fries)', 22.3, 61.771, 0.061771),
(86, 'Lipa', '2020', 'July', 'RGO', '1 Hot Snack (burger and fries)', 9.4, 26.038, 0.026038),
(87, 'Lipa', '2020', 'August', 'Procurement', 'Meal with Chicken', 9, 30.51, 0.030510000000000002),
(88, 'Lipa', '2020', 'September', 'Auxillary Services', '1 Sandwich', 5.9, 7.493, 0.0074930000000000005),
(90, 'Lipa', '2020', 'October', 'Auxillary Services', '1 Average Meal', 6.9, 32.43, 0.03243),
(91, 'Lipa', '2020', 'November', 'Auxillary Services', '1 Cold or Hot Snack', 13, 26.26, 0.026260000000000002),
(92, 'Lipa', '2020', 'December', 'Auxillary Services', '1 Hot Snack (burger and fries)', 13.3, 36.841, 0.036841),
(93, 'Lipa', '2021', 'January', 'Procurement', '1 Hot Snack (burger and fries)', 19.7, 54.568999999999996, 0.05456899999999999),
(94, 'Lipa', '2021', 'February', 'Auxillary Services', '1 Cold or Hot Snack', 13.6, 27.471999999999998, 0.027471999999999996),
(95, 'Lipa', '2021', 'March', 'Auxillary Services', 'Meal,Vegetarian', 17, 48.45, 0.04845),
(96, 'Lipa', '2021', 'April', 'Auxillary Services', 'Meal,Vegan', 20.5, 34.644999999999996, 0.034644999999999995),
(97, 'Lipa', '2021', 'May', 'RGO', '1 Hot Snack (burger and fries)', 16.9, 46.812999999999995, 0.046812999999999994),
(98, 'Lipa', '2021', 'June', 'Procurement', '1 Average Meal', 30.2, 141.94, 0.14194),
(99, 'Lipa', '2021', 'July', 'Procurement', '1 Cold or Hot Snack', 28.4, 57.367999999999995, 0.057367999999999995),
(100, 'Lipa', '2021', 'August', 'Procurement', '1 Gourmet Breakfast', 30.2, 70.366, 0.070366),
(101, 'Lipa', '2021', 'September', 'Procurement', 'Meal,Vegetarian', 7.8, 22.23, 0.02223),
(102, 'Lipa', '2021', 'October', 'Procurement', '1 Hot Snack (burger and fries)', 5.2, 14.404, 0.014404),
(103, 'Lipa', '2021', 'November', 'Auxillary Services', 'Meal with Beef', 9, 62.37, 0.062369999999999995),
(104, 'Lipa', '2021', 'December', 'Procurement', '1 Average Meal', 12.8, 60.160000000000004, 0.060160000000000005),
(105, 'Lipa', '2022', 'January', 'Auxillary Services', '1 Cold or Hot Snack', 13.8, 27.876, 0.027876),
(106, 'Lipa', '2022', 'February', 'Auxillary Services', '1 Standard Breakfast', 30.1, 25.284, 0.025283999999999997),
(107, 'Lipa', '2022', 'March', 'Procurement', '1 Hot Snack (burger and fries)', 23.4, 64.818, 0.064818),
(108, 'Lipa', '2022', 'April', 'Auxillary Services', '1 Hot Snack (burger and fries)', 17.6, 48.752, 0.048752000000000004),
(109, 'Lipa', '2022', 'May', 'Auxillary Services', '1 Average Meal', 12.5, 58.75, 0.05875),
(110, 'Lipa', '2022', 'June', 'Procurement', 'Meal,Vegetarian', 11.8, 33.63, 0.03363),
(111, 'Lipa', '2022', 'July', 'Procurement', '1 Hot Snack (burger and fries)', 6.8, 18.836, 0.018836),
(112, 'Lipa', '2022', 'August', 'Procurement', '1 Hot Snack (burger and fries)', 9.2, 25.483999999999998, 0.025484),
(113, 'Lipa', '2022', 'September', 'Procurement', '1 Standard Breakfast', 10.7, 8.988, 0.008988),
(114, 'Lipa', '2022', 'October', 'Procurement', '1 Sandwich', 12.8, 16.256, 0.016256),
(115, 'Lipa', '2022', 'November', 'Auxillary Services', '1 Hot Snack (burger and fries)', 18.9, 52.352999999999994, 0.052353),
(116, 'Lipa', '2022', 'December', 'Procurement', '1 Standard Breakfast', 12.4, 10.416, 0.010416),
(117, 'Lipa', '2023', 'January', 'Auxillary Services', '1 Hot Snack (burger and fries)', 10.25, 28.392500000000002, 0.0283925),
(118, 'Lipa', '2023', 'February', 'Auxillary Services', '1 Standard Breakfast', 33.5, 28.14, 0.028140000000000002),
(119, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Hot Snack (burger and fries)', 30.5, 84.485, 0.084485),
(120, 'Lipa', '2023', 'April', 'Auxillary Services', '1 Cold or Hot Snack', 30.5, 61.61, 0.06161),
(121, 'Lipa', '2023', 'May', 'Procurement', '1 Sandwich', 34, 43.18, 0.04318),
(122, 'Lipa', '2023', 'June', 'Procurement', '1 Hot Snack (burger and fries)', 11, 30.47, 0.03047),
(123, 'Lipa', '2023', 'July', 'Auxillary Services', '1 Hot Snack (burger and fries)', 8.25, 22.8525, 0.022852499999999998),
(124, 'Lipa', '2023', 'August', 'Procurement', '1 Hot Snack (burger and fries)', 9.5, 26.315, 0.026315),
(125, 'Lipa', '2023', 'September', 'Procurement', '1 Hot Snack (burger and fries)', 6.75, 18.6975, 0.018697500000000002),
(126, 'Lipa', '2023', 'October', 'Auxillary Services', '1 Hot Snack (burger and fries)', 6.5, 18.005, 0.018005),
(127, 'Lipa', '2023', 'November', 'Procurement', '1 Hot Snack (burger and fries)', 14, 38.78, 0.03878),
(128, 'Lipa', '2023', 'December', 'Procurement', '1 Cold or Hot Snack', 15, 30.3, 0.0303),
(129, 'Lipa', '2024', 'January', 'Procurement', '1 Hot Snack (burger and fries)', 11.5, 31.855, 0.031855),
(130, 'Lipa', '2024', 'February', 'Auxillary Services', '1 Cold or Hot Snack', 20, 40.4, 0.0404),
(131, 'Lipa', '2024', 'March', 'Auxillary Services', 'Meal with Chicken', 10.25, 34.7475, 0.0347475),
(132, 'Lipa', '2024', 'April', 'Auxillary Services', '1 Average Meal', 15, 70.5, 0.0705),
(133, 'Lipa', '2024', 'May', 'Procurement', '1 Hot Snack (burger and fries)', 13.5, 37.395, 0.037395000000000005),
(134, 'Lipa', '2024', 'June', 'Auxillary Services', '1 Hot Snack (burger and fries)', 5.5, 15.235, 0.015235),
(135, 'Lipa', '2019', 'January', 'Procurement', 'Meal,Vegan', 34, 57.46, 0.057460000000000004),
(136, 'Lipa', '2019', 'February', 'Procurement', '1 Cold or Hot Snack', 89, 179.78, 0.17978),
(137, 'Lipa', '2019', 'March', 'Auxillary Services', '1 Hot Snack (burger and fries)', 45, 124.65, 0.12465000000000001),
(138, 'Lipa', '2019', 'April', 'Procurement', 'Meal with Beef', 32, 221.76, 0.22175999999999998),
(139, 'Lipa', '2019', 'May', 'Procurement', '1 Gourmet Breakfast', 45, 104.85000000000001, 0.10485000000000001),
(140, 'Lipa', '2019', 'June', 'Procurement', '1 Standard Breakfast', 67, 56.28, 0.056280000000000004),
(141, 'Lipa', '2019', 'July', 'Procurement', '1 Gourmet Breakfast', 45, 104.85000000000001, 0.10485000000000001),
(142, 'Lipa', '2019', 'August', 'Procurement', '1 Average Meal', 99, 465.3, 0.4653),
(143, 'Lipa', '2019', 'September', 'RGO', 'Meal with Chicken', 123, 416.97, 0.41697),
(144, 'Lipa', '2019', 'October', 'Auxillary Services', '1 Gourmet Breakfast', 98, 228.34, 0.22834000000000002),
(145, 'Lipa', '2019', 'November', 'RGO', '1 Average Meal', 56, 263.2, 0.2632),
(146, 'Lipa', '2019', 'December', 'Procurement', 'Meal,Vegetarian', 12, 34.2, 0.0342);

-- --------------------------------------------------------

--
-- Table structure for table `tbllpg`
--

CREATE TABLE `tbllpg` (
  `id` int(11) NOT NULL,
  `Campus` char(20) DEFAULT NULL,
  `Office` char(20) DEFAULT NULL,
  `YearTransact` year(4) DEFAULT NULL,
  `Month` varchar(20) DEFAULT NULL,
  `ConcessionariesType` varchar(20) DEFAULT NULL,
  `TankQuantity` int(11) DEFAULT NULL,
  `TankWeight` float DEFAULT NULL,
  `TankVolume` float DEFAULT NULL,
  `TotalTankVolume` float DEFAULT NULL,
  `GHGEmissionKGCO2e` float DEFAULT NULL,
  `GHGEmissionTCO2e` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbllpg`
--

INSERT INTO `tbllpg` (`id`, `Campus`, `Office`, `YearTransact`, `Month`, `ConcessionariesType`, `TankQuantity`, `TankWeight`, `TankVolume`, `TotalTankVolume`, `GHGEmissionKGCO2e`, `GHGEmissionTCO2e`) VALUES
(139, 'Lipa', 'Procurement', '2020', 'January', 'Fuel', 45, 21, 41.16, 1852.2, 62.117, 0.062117),
(140, 'Lipa', 'Auxiliary Services', '2020', 'February', 'Fuel', 78, 110, 215.6, 16816.8, 325.375, 0.325375),
(141, 'Lipa', 'Auxiliary Services', '2020', 'March', 'Fuel', 34, 200, 392, 13328, 591.59, 0.59159),
(142, 'Lipa', 'Auxiliary Services', '2020', 'April', 'Fuel', 104, 700, 1372, 142688, 2070.56, 2.07056),
(143, 'Lipa', 'Auxiliary Services', '2020', 'May', 'Fuel', 90, 200, 392, 35280, 591.59, 0.59159),
(144, 'Lipa', 'Procurement', '2020', 'June', 'Diesel', 88, 345, 676.2, 59505.6, 1020.49, 1.02049),
(145, 'Lipa', 'RGO', '2020', 'July', 'Fuel', 99, 490, 960.4, 95079.6, 1449.4, 1.4494),
(146, 'Lipa', 'Auxiliary Services', '2020', 'August', 'Diesel', 45, 300, 588, 26460, 887.385, 0.887385),
(147, 'Lipa', 'RGO', '2020', 'September', 'Fuel', 30, 405, 793.8, 23814, 1197.97, 1.19797),
(148, 'Lipa', 'Auxiliary Services', '2020', 'October', 'Fuel', 20, 600, 1176, 23520, 1774.77, 1.77477),
(149, 'Lipa', 'Auxiliary Services', '2020', 'November', 'Fuel', 35, 650, 1274, 44590, 1922.67, 1.92267),
(150, 'Lipa', 'Auxiliary Services', '2020', 'December', 'Fuel', 67, 780, 1528.8, 102430, 2307.2, 2.3072),
(151, 'Lipa', 'Auxiliary Services', '2021', 'January', 'Fuel', 78, 880, 1724.8, 134534, 2603, 2.603),
(152, 'Lipa', 'RGO', '2021', 'February', 'Fuel', 60, 560, 1097.6, 65856, 1656.45, 1.65645),
(153, 'Lipa', 'RGO', '2021', 'March', 'Fuel', 45, 770, 1509.2, 67914, 2277.62, 2.27762),
(154, 'Lipa', 'Procurement', '2021', 'April', 'Diesel', 60, 680, 1332.8, 79968, 2011.41, 2.01141),
(155, 'Lipa', 'Procurement', '2021', 'May', 'Fuel', 56, 700, 1372, 76832, 2070.56, 2.07056),
(156, 'Lipa', 'Procurement', '2021', 'June', 'Diesel', 67, 890, 1744.4, 116875, 2632.58, 2.63258),
(157, 'Lipa', 'RGO', '2021', 'July', 'Fuel', 99, 1120, 2195.2, 217325, 3312.9, 3.3129),
(158, 'Lipa', 'Auxiliary Services', '2021', 'August', 'Diesel', 89, 1009, 1977.64, 176010, 2984.57, 2.98457),
(159, 'Lipa', 'Auxiliary Services', '2021', 'September', 'Fuel', 77, 870, 1705.2, 131300, 2573.42, 2.57342),
(160, 'Lipa', 'RGO', '2021', 'October', 'Fuel', 90, 980, 1920.8, 172872, 2898.79, 2.89879),
(161, 'Lipa', 'Auxiliary Services', '2021', 'November', 'Fuel', 67, 750, 1470, 98490, 2218.46, 2.21846),
(162, 'Lipa', 'Procurement', '2021', 'December', 'Fuel', 56, 689, 1350.44, 75624.6, 2038.03, 2.03803),
(163, 'Lipa', 'Procurement', '2022', 'January', 'Fuel', 45, 550, 1078, 48510, 1626.87, 1.62687),
(164, 'Lipa', 'Auxiliary Services', '2022', 'February', 'Diesel', 43, 560, 1097.6, 47196.8, 1656.45, 1.65645),
(165, 'Lipa', 'Auxiliary Services', '2022', 'March', 'Fuel', 67, 776, 1520.96, 101904, 2295.37, 2.29537),
(166, 'Lipa', 'Auxiliary Services', '2022', 'April', 'Fuel', 35, 440, 862.4, 30184, 1301.5, 1.3015),
(167, 'Lipa', 'Procurement', '2022', 'May', 'Fuel', 67, 887, 1738.52, 116481, 2623.7, 2.6237),
(168, 'Lipa', 'RGO', '2022', 'June', 'Fuel', 46, 780, 1528.8, 70324.8, 2307.2, 2.3072),
(169, 'Lipa', 'Auxiliary Services', '2022', 'July', 'Fuel', 34, 780, 1528.8, 51979.2, 2307.2, 2.3072),
(170, 'Lipa', 'Procurement', '2022', 'August', 'Fuel', 55, 890, 1744.4, 95942, 2632.58, 2.63258),
(171, 'Lipa', 'Procurement', '2022', 'September', 'Fuel', 32, 890, 1744.4, 55820.8, 2632.58, 2.63258),
(172, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Fuel', 54, 670, 1313.2, 70912.8, 1981.83, 1.98183),
(173, 'Lipa', 'Procurement', '2022', 'November', 'Fuel', 32, 670, 1313.2, 42022.4, 1981.83, 1.98183),
(174, 'Lipa', 'Procurement', '2022', 'December', 'Fuel', 45, 987, 1934.52, 87053.4, 2919.5, 2.9195),
(175, 'Lipa', 'Auxiliary Services', '2023', 'January', 'Fuel', 56, 890.98, 1746.32, 97794, 2635.47, 2.63547),
(176, 'Lipa', 'Auxiliary Services', '2023', 'February', 'Fuel', 67, 882, 1728.72, 115824, 2608.91, 2.60891),
(177, 'Lipa', 'Procurement', '2023', 'March', 'Diesel', 65, 890, 1744.4, 113386, 2632.58, 2.63258),
(178, 'Lipa', 'Auxiliary Services', '2023', 'April', 'Fuel', 56, 990, 1940.4, 108662, 2928.37, 2.92837),
(179, 'Lipa', 'Procurement', '2023', 'May', 'Fuel', 102, 1456, 2853.76, 291084, 4306.78, 4.30678),
(180, 'Lipa', 'Auxiliary Services', '2023', 'June', 'Fuel', 108, 1543, 3024.28, 326622, 4564.12, 4.56412),
(181, 'Lipa', 'Auxiliary Services', '2023', 'July', 'Fuel', 123, 1321, 2589.16, 318467, 3907.45, 3.90745),
(182, 'Lipa', 'Procurement', '2023', 'August', 'Fuel', 111, 1785.55, 3499.68, 388464, 5281.57, 5.28157),
(183, 'Lipa', 'Auxiliary Services', '2023', 'September', 'Fuel', 67, 780, 1528.8, 102430, 2307.2, 2.3072),
(184, 'Lipa', 'Procurement', '2023', 'October', 'Fuel', 56, 670, 1313.2, 73539.2, 1981.83, 1.98183),
(185, 'Lipa', 'RGO', '2023', 'November', 'Fuel', 56, 680, 1332.8, 74636.8, 2011.41, 2.01141),
(186, 'Lipa', 'Procurement', '2023', 'December', 'Diesel', 56, 790, 1548.4, 86710.4, 2336.78, 2.33678),
(187, 'Lipa', 'Procurement', '2024', 'January', 'Fuel', 78, 988, 1936.48, 151045, 2922.45, 2.92245),
(188, 'Lipa', 'RGO', '2024', 'February', 'Diesel', 78, 784, 1536.64, 119858, 2319.03, 2.31903),
(189, 'Lipa', 'Procurement', '2024', 'March', 'Diesel', 40, 800, 1568, 62720, 2366.36, 2.36636),
(190, 'Lipa', 'Auxiliary Services', '2024', 'April', 'Fuel', 56, 780, 1528.8, 85612.8, 2307.2, 2.3072),
(191, 'Lipa', 'Procurement', '2024', 'May', 'Fuel', 67, 835, 1636.6, 109652, 2469.89, 2.46989),
(192, 'Lipa', 'Procurement', '2024', 'June', 'Fuel', 56, 780, 1528.8, 85612.8, 2307.2, 2.3072);

-- --------------------------------------------------------

--
-- Table structure for table `tblsignin`
--

CREATE TABLE `tblsignin` (
  `userID` int(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `office` varchar(255) NOT NULL,
  `campus` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblsignin`
--

INSERT INTO `tblsignin` (`userID`, `username`, `office`, `campus`, `email`, `password`) VALUES
(34, 'csd', 'Central Sustainable Office', 'Central', 'central@gmail.com', 'csd1'),
(45, 'sdo-alangilan', 'Sustainable Development Office', 'Alangilan', 'sdoalangilan@gmail.com', 'sdoalangilan1'),
(67, 'sdo-nasugbu', 'Sustainable Development Office', 'ARASOF-Nasugbu', 'sdonasugbu@gmail.com', 'sdonasugbu1'),
(68, 'sdo-balayan', 'Sustainable Development Office', 'Balayan', 'sdobalayan@gmail.com', 'sdobalayan1'),
(69, 'sdo-central', 'Sustainable Development Office', 'Central', 'sdocentral@gmail.com', 'sdocentral1'),
(70, 'sdo-malvar', 'Sustainable Development Office', 'JPLPC-Malvar', 'sdomalvar@gmail.com', 'sdomalvar1'),
(71, 'sdo-lemery', 'Sustainable Development Office', 'Lemery', 'sdolemery@gmail.com', 'sdolemery1'),
(72, 'sdo-lipa', 'Sustainable Development Office', 'Lipa', 'sdolipa@gmail.com', 'sdolipa1'),
(73, 'sdo-lobo', 'Sustainable Development Office', 'Lobo', 'sdolobo@gmail.com', 'sdolobo1'),
(74, 'sdo-mabini', 'Sustainable Development Office', 'Mabini', 'sdomabini@gmail.com', 'sdomabini1'),
(75, 'sdo-pabloborbon', 'Sustainable Development Office', 'Pablo Borbon', 'sdopabloborbon@gmail.com', 'sdopabloborbon1'),
(76, 'sdo-rosario', 'Sustainable Development Office', 'Rosario', 'sdorosario@gmail.com', 'sdorosario1'),
(77, 'sdo-sanjuan', 'Sustainable Development Office', 'San Juan', 'sdosanjuan@gmail.com', 'sdosanjuan1'),
(78, 'emu-alangilan', 'Environmental Management Unit', 'Alangilan', 'emualangilan@gmail.com', 'emualangilan1'),
(79, 'emu-nasugbu', 'Environmental Management Unit', 'ARASOF-Nasugbu', 'emunasugbu@gmail.com', 'emunasugbu1'),
(80, 'emu-balayan', 'Environmental Management Unit', 'Balayan', 'emubalayan@gmail.com', 'emubalayan1'),
(81, 'emu-central', 'Environmental Management Unit', 'Central', 'emucentral@gmail.com', 'emucentral1'),
(82, 'emu-malvar', 'Environmental Management Unit', 'JPLPC-Malvar', 'emumalvar@gmail.com', 'emumalvar1'),
(83, 'emu-lemery', 'Environmental Management Unit', 'Lemery', 'emulemery@gmail.com', 'emulemery1'),
(84, 'emu-lipa', 'Environmental Management Unit', 'Lipa', 'emulipa@gmail.com', 'emulipa1'),
(86, 'emu-lobo', 'Environmental Management Unit', 'Lobo', 'emulobo@gmail.com', 'emulobo1'),
(87, 'emu-mabini', 'Environmental Management Unit', 'Mabini', 'emumabini@gmail.com', 'emumabini1'),
(88, 'emu-pabloborbon', 'Environmental Management Unit', 'Pablo Borbon', 'emupabloborbon@gmail.com', 'emupabloborbon1'),
(89, 'emu-rosario', 'Environmental Management Unit', 'Rosario', 'emurosario@gmail.com', 'emurosario1'),
(90, 'emu-sanjuan', 'Environmental Management Unit', 'San Juan', 'emusanjuan@gmail.com', 'emusanjuan1'),
(91, 'po-alangilan', 'Procurement Office', 'Alangilan', 'poalangilan@gmail.com', 'poalangilan1'),
(92, 'po-nasugbu', 'Procurement Office', 'ARASOF-Nasugbu', 'ponasugbu@gmail.com', 'ponasugbu1'),
(93, 'po-balayan', 'Procurement Office', 'Balayan', 'pobalayan@gmail.com', 'pobalayan1'),
(94, 'po-central', 'Procurement Office', 'Central', 'pocentral@gmail.com', 'pocentral1'),
(95, 'po-malvar', 'Procurement Office', 'JPLPC-Malvar', 'pomalvar@gmail.com', 'pomalvar1'),
(96, 'po-lemery', 'Procurement Office', 'Lemery', 'polemery@gmail.com', 'polemery1'),
(97, 'po-lipa', 'Procurement Office', 'Lipa', 'polipa@gmail.com', 'polipa1'),
(98, 'po-lobo', 'Procurement Office', 'Lobo', 'polobo@gmail.com', 'polobo1'),
(99, 'po-mabini', 'Procurement Office', 'Mabini', 'pomabini@gmail.com', 'pomabini1'),
(100, 'po-pabloborbon', 'Procurement Office', 'Pablo Borbon', 'popabloborbon@gmail.com', 'popabloborbon1'),
(101, 'po-rosario', 'Procurement Office', 'Rosario', 'porosario@gmail.com', 'porosario1'),
(102, 'po-sanjuan', 'Procurement Office', 'San Juan', 'posanjuan@gmail.com', 'posanjuan1'),
(103, 'ea-alangilan', 'External Affair', 'Alangilan', 'eaalangilan@gmail.com', 'eaalangilan1'),
(104, 'ea-nasugbu', 'External Affair', 'ARASOF-Nasugbu', 'eanasugbu@gmail.com', 'eanasugbu1'),
(105, 'ea-balayan', 'External Affair', 'Balayan', 'eabalayan@gmail.com', 'eabalayan1'),
(106, 'ea-central', 'External Affair', 'Central', 'eacentral@gmail.com', 'eacentral1'),
(107, 'ea-malvar', 'External Affair', 'JPLPC-Malvar', 'eamalvar@gmail.com', 'eamalvar1'),
(108, 'ea-lemery', 'External Affair', 'Lemery', 'ealemery@gmail.com', 'ealemery1'),
(109, 'ea-lipa', 'External Affair', 'Lipa', 'ealipa@gmail.com', 'ealipa1'),
(110, 'ea-lobo', 'External Affair', 'Lobo', 'ealobo@gmail.com', 'ealobo1'),
(111, 'ea-mabini', 'External Affair', 'Mabini', 'eamabini@gmail.com', 'eamabini1'),
(112, 'ea-pabloborbon', 'External Affair', 'Pablo Borbon', 'eapabloborbon@gmail.com', 'eapabloborbon1'),
(113, 'ea-rosario', 'External Affair', 'Rosario', 'earosario@gmail.com', 'earosario1'),
(114, 'ea-sanjuan', 'External Affair', 'San Juan', 'easanjuan@gmail.com', 'easanjuan1');

-- --------------------------------------------------------

--
-- Table structure for table `tblsolidwastesegregated`
--

CREATE TABLE `tblsolidwastesegregated` (
  `id` int(11) NOT NULL,
  `Campus` char(20) DEFAULT NULL,
  `Year` int(11) DEFAULT NULL,
  `Quarter` varchar(20) DEFAULT NULL,
  `Month` varchar(20) DEFAULT NULL,
  `MainCategory` varchar(30) DEFAULT NULL,
  `SubCategory` varchar(30) DEFAULT NULL,
  `QuantityInKG` float DEFAULT NULL,
  `GHGEmissionKGCO2e` float DEFAULT NULL,
  `GHGEmissionTCO2e` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblsolidwastesegregated`
--

INSERT INTO `tblsolidwastesegregated` (`id`, `Campus`, `Year`, `Quarter`, `Month`, `MainCategory`, `SubCategory`, `QuantityInKG`, `GHGEmissionKGCO2e`, `GHGEmissionTCO2e`) VALUES
(77, 'Lipa', 2024, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 146.5, 91.8365, 0.0918365),
(78, 'Lipa', 2024, 'Q1', 'March', 'biodegradable', 'BiodegradableFood Waste', 112, 70.2094, 0.0702094),
(79, 'Lipa', 2024, 'Q1', 'January', 'residual', 'ResidualResidual', 203, 90.5867, 0.0905867),
(80, 'Lipa', 2024, 'Q1', 'February', 'residual', 'ResidualResidual', 411, 183.405, 0.183405),
(81, 'Lipa', 2024, 'Q1', 'March', 'residual', 'ResidualResidual', 354.5, 158.192, 0.158192),
(82, 'Lipa', 2024, 'Q1', 'January', 'recyclable', 'RecyclableMixed Metal', 6, 0.0534, 0.0000534),
(83, 'Lipa', 2024, 'Q1', 'February', 'recyclable', 'RecyclableMixed Paper', 11.75, 12.2411, 0.0122412),
(84, 'Lipa', 2024, 'Q1', 'March', 'recyclable', 'RecyclableMixed Paper', 8.25, 8.59485, 0.00859485),
(85, 'Lipa', 2024, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 102, 63.9407, 0.0639407),
(86, 'Lipa', 2024, 'Q2', 'May', 'biodegradable', 'BiodegradableFood Waste', 94, 58.9258, 0.0589258),
(87, 'Lipa', 2024, 'Q2', 'June', 'biodegradable', 'BiodegradableFood Waste', 44, 27.5823, 0.0275823),
(88, 'Lipa', 2024, 'Q2', 'April', 'residual', 'ResidualResidual', 475, 211.964, 0.211964),
(89, 'Lipa', 2024, 'Q2', 'May', 'residual', 'ResidualResidual', 488, 217.765, 0.217765),
(90, 'Lipa', 2024, 'Q2', 'June', 'residual', 'ResidualResidual', 151.45, 67.583, 0.067583),
(91, 'Lipa', 2024, 'Q2', 'April', 'recyclable', 'RecyclableMixed Plastic', 12.5, 0.11125, 0.00011125),
(92, 'Lipa', 2024, 'Q2', 'May', 'recyclable', 'RecyclableMixed Paper', 8.75, 9.11575, 0.00911575),
(93, 'Lipa', 2024, 'Q2', 'June', 'recyclable', 'RecyclableMixed Metal', 4.3, 0.03827, 0.00003827),
(94, 'Lipa', 2023, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 463, 290.241, 0.290241),
(95, 'Lipa', 2023, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 168.25, 105.471, 0.105471),
(96, 'Lipa', 2023, 'Q1', 'March', 'biodegradable', 'BiodegradableFood Waste', 96.5, 60.493, 0.060493),
(97, 'Lipa', 2023, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 98, 61.4333, 0.0614333),
(98, 'Lipa', 2023, 'Q2', 'May', 'biodegradable', 'BiodegradableFood Waste', 271.5, 170.195, 0.170195),
(99, 'Lipa', 2023, 'Q2', 'June', 'biodegradable', 'BiodegradableFood Waste', 49.5, 31.0301, 0.0310301),
(100, 'Lipa', 2023, 'Q3', 'July', 'biodegradable', 'BiodegradableFood Waste', 119, 74.5975, 0.0745975),
(101, 'Lipa', 2023, 'Q3', 'August', 'biodegradable', 'BiodegradableFood Waste', 129.5, 81.1797, 0.0811797),
(102, 'Lipa', 2023, 'Q3', 'August', 'biodegradable', 'BiodegradableFood Waste', 129.5, 81.1797, 0.0811797),
(103, 'Lipa', 2023, 'Q3', 'September', 'biodegradable', 'BiodegradableFood Waste', 64.5, 40.4331, 0.0404331),
(104, 'Lipa', 2023, 'Q3', 'October', 'biodegradable', 'BiodegradableFood Waste', 46.5, 29.1495, 0.0291495),
(105, 'Lipa', 2023, 'Q4', 'November', 'biodegradable', 'BiodegradableFood Waste', 48, 30.0898, 0.0300898),
(106, 'Lipa', 2023, 'Q4', 'December', 'biodegradable', 'BiodegradableFood Waste', 77.5, 48.5824, 0.0485824),
(107, 'Lipa', 2023, 'Q1', 'January', 'residual', 'ResidualResidual', 203, 90.5867, 0.0905867),
(108, 'Lipa', 2023, 'Q1', 'February', 'residual', 'ResidualResidual', 519, 231.599, 0.231599),
(109, 'Lipa', 2023, 'Q1', 'March', 'residual', 'ResidualResidual', 389, 173.587, 0.173587),
(110, 'Lipa', 2023, 'Q2', 'April', 'residual', 'ResidualResidual', 319, 142.351, 0.142351),
(111, 'Lipa', 2023, 'Q2', 'May', 'residual', 'ResidualResidual', 482, 215.088, 0.215088),
(112, 'Lipa', 2023, 'Q2', 'June', 'residual', 'ResidualResidual', 140, 62.4736, 0.0624736),
(113, 'Lipa', 2023, 'Q3', 'July', 'residual', 'ResidualResidual', 209, 93.2642, 0.0932642),
(114, 'Lipa', 2023, 'Q3', 'August', 'residual', 'ResidualResidual', 316, 141.012, 0.141012),
(115, 'Lipa', 2023, 'Q3', 'September', 'residual', 'ResidualResidual', 207, 92.3717, 0.0923717),
(116, 'Lipa', 2023, 'Q4', 'October', 'residual', 'ResidualResidual', 205, 91.4792, 0.0914792),
(117, 'Lipa', 2023, 'Q4', 'November', 'residual', 'ResidualResidual', 338.45, 151.03, 0.15103),
(118, 'Lipa', 2023, 'Q4', 'December', 'residual', 'ResidualResidual', 265.5, 118.477, 0.118477),
(119, 'Lipa', 2023, 'Q1', 'January', 'recyclable', 'RecyclableMixed Plastic', 24, 0.2136, 0.0002136),
(120, 'Lipa', 2023, 'Q2', 'February', 'recyclable', 'RecyclableMixed Plastic', 30.25, 0.269225, 0.000269225),
(121, 'Lipa', 2023, 'Q1', 'March', 'recyclable', 'RecyclableMixed Plastic', 13.75, 0.122375, 0.000122375),
(122, 'Lipa', 2023, 'Q2', 'April', 'recyclable', 'RecyclableMixed Plastic', 13.5, 0.12015, 0.00012015),
(123, 'Lipa', 2023, 'Q2', 'May', 'recyclable', 'RecyclableMixed Plastic', 13.75, 0.122375, 0.000122375),
(124, 'Lipa', 2023, 'Q2', 'June', 'recyclable', 'RecyclableMixed Plastic', 2.25, 0.020025, 0.000020025),
(125, 'Lipa', 2023, 'Q3', 'July', 'recyclable', 'RecyclableMixed Plastic', 2, 0.0178, 0.0000178),
(126, 'Lipa', 2023, 'Q3', 'August', 'recyclable', 'RecyclableMixed Plastic', 3.75, 0.033375, 0.000033375),
(127, 'Lipa', 2023, 'Q3', 'September', 'recyclable', 'RecyclableMixed Plastic', 2.2, 0.01958, 0.00001958),
(128, 'Lipa', 2023, 'Q4', 'October', 'recyclable', 'RecyclableMixed Plastic', 2, 0.0178, 0.0000178),
(129, 'Lipa', 2023, 'Q4', 'November', 'recyclable', 'RecyclableMixed Plastic', 4.75, 0.042275, 0.000042275),
(130, 'Lipa', 2023, 'Q4', 'December', 'recyclable', 'RecyclableMixed Plastic', 2.5, 0.02225, 0.00002225),
(131, 'Lipa', 2022, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 471, 295.256, 0.295256),
(132, 'Lipa', 2022, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 471, 295.256, 0.295256),
(133, 'Lipa', 2022, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 178.52, 111.909, 0.111909),
(134, 'Lipa', 2022, 'Q2', 'March', 'biodegradable', 'BiodegradableFood Waste', 93.37, 58.5309, 0.0585309),
(135, 'Lipa', 2022, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 101.21, 63.4455, 0.0634455),
(136, 'Lipa', 2022, 'Q2', 'May', 'biodegradable', 'BiodegradableFood Waste', 263, 164.867, 0.164867),
(137, 'Lipa', 2022, 'Q2', 'June', 'biodegradable', 'BiodegradableFood Waste', 50.25, 31.5002, 0.0315002),
(138, 'Lipa', 2022, 'Q3', 'July', 'biodegradable', 'BiodegradableFood Waste', 125, 78.3587, 0.0783587),
(139, 'Lipa', 2022, 'Q3', 'August', 'biodegradable', 'BiodegradableFood Waste', 135.62, 85.0161, 0.0850161),
(140, 'Lipa', 2022, 'Q3', 'September', 'biodegradable', 'BiodegradableFood Waste', 70.26, 44.0439, 0.0440439),
(141, 'Lipa', 2022, 'Q4', 'October', 'biodegradable', 'BiodegradableFood Waste', 65.14, 40.8343, 0.0408343),
(142, 'Lipa', 2022, 'Q4', 'November', 'biodegradable', 'BiodegradableFood Waste', 50.19, 31.4626, 0.0314626),
(143, 'Lipa', 2022, 'Q4', 'December', 'biodegradable', 'BiodegradableFood Waste', 80.05, 50.1809, 0.0501809),
(144, 'Lipa', 2022, 'Q1', 'January', 'residual', 'ResidualResidual', 211, 94.1566, 0.0941566),
(145, 'Lipa', 2022, 'Q1', 'February', 'residual', 'ResidualResidual', 515, 229.814, 0.229814),
(146, 'Lipa', 2022, 'Q1', 'March', 'residual', 'ResidualResidual', 377, 168.232, 0.168232),
(147, 'Lipa', 2022, 'Q2', 'April', 'residual', 'ResidualResidual', 288, 128.517, 0.128517),
(148, 'Lipa', 2022, 'Q2', 'May', 'residual', 'ResidualResidual', 452.35, 201.857, 0.201857),
(149, 'Lipa', 2022, 'Q2', 'June', 'residual', 'ResidualResidual', 132, 58.9037, 0.0589037),
(150, 'Lipa', 2022, 'Q3', 'July', 'residual', 'ResidualResidual', 188, 83.8931, 0.0838931),
(151, 'Lipa', 2022, 'Q3', 'August', 'residual', 'ResidualResidual', 314.73, 140.445, 0.140445),
(152, 'Lipa', 2022, 'Q3', 'September', 'residual', 'ResidualResidual', 208.28, 92.9429, 0.0929429),
(153, 'Lipa', 2022, 'Q4', 'October', 'residual', 'ResidualResidual', 206.92, 92.336, 0.092336),
(154, 'Lipa', 2022, 'Q4', 'November', 'residual', 'ResidualResidual', 332.54, 148.393, 0.148393),
(155, 'Lipa', 2022, 'Q4', 'December', 'residual', 'ResidualResidual', 276.72, 123.484, 0.123484),
(156, 'Lipa', 2022, 'Q1', 'January', 'recyclable', 'RecyclableMixed Plastic', 25, 0.2225, 0.0002225),
(157, 'Lipa', 2022, 'Q1', 'February', 'recyclable', 'RecyclableMixed Plastic', 31.94, 0.284266, 0.000284266),
(158, 'Lipa', 2022, 'Q2', 'March', 'recyclable', 'RecyclableMixed Plastic', 12.97, 0.115433, 0.000115433),
(159, 'Lipa', 2022, 'Q2', 'April', 'recyclable', 'RecyclableMixed Plastic', 13.49, 0.120061, 0.000120061),
(160, 'Lipa', 2022, 'Q2', 'May', 'recyclable', 'RecyclableMixed Plastic', 14.71, 0.130919, 0.000130919),
(161, 'Lipa', 2022, 'Q2', 'June', 'recyclable', 'RecyclableMixed Plastic', 2.3, 0.02047, 0.00002047),
(162, 'Lipa', 2022, 'Q3', 'July', 'recyclable', 'RecyclableMixed Plastic', 2.13, 0.018957, 0.000018957),
(163, 'Lipa', 2022, 'Q3', 'August', 'recyclable', 'RecyclableMixed Plastic', 3.41, 0.030349, 0.000030349),
(164, 'Lipa', 2022, 'Q3', 'September', 'recyclable', 'RecyclableMixed Plastic', 2.32, 0.020648, 0.000020648),
(165, 'Lipa', 2022, 'Q4', 'October', 'recyclable', 'RecyclableMixed Plastic', 1.97, 0.017533, 0.000017533),
(166, 'Lipa', 2022, 'Q4', 'November', 'recyclable', 'RecyclableMixed Plastic', 4.36, 0.038804, 0.000038804),
(167, 'Lipa', 2022, 'Q4', 'December', 'recyclable', 'RecyclableMixed Plastic', 2.71, 0.024119, 0.000024119),
(168, 'Lipa', 2021, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 420.22, 263.423, 0.263423),
(169, 'Lipa', 2021, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 159.51, 99.992, 0.099992),
(170, 'Lipa', 2021, 'Q1', 'March', 'biodegradable', 'BiodegradableFood Waste', 94.39, 59.1703, 0.0591703),
(171, 'Lipa', 2021, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 89.84, 56.318, 0.056318),
(172, 'Lipa', 2021, 'Q2', 'May', 'biodegradable', 'BiodegradableFood Waste', 260.51, 163.306, 0.163306),
(173, 'Lipa', 2021, 'Q2', 'June', 'biodegradable', 'BiodegradableFood Waste', 47.48, 29.7638, 0.0297638),
(174, 'Lipa', 2021, 'Q3', 'July', 'biodegradable', 'BiodegradableFood Waste', 112.25, 70.3662, 0.0703662),
(175, 'Lipa', 2021, 'Q3', 'August', 'biodegradable', 'BiodegradableFood Waste', 116.95, 73.3124, 0.0733124),
(176, 'Lipa', 2021, 'Q3', 'September', 'biodegradable', 'BiodegradableFood Waste', 61.56, 38.5901, 0.0385901),
(177, 'Lipa', 2021, 'Q4', 'October', 'biodegradable', 'BiodegradableFood Waste', 42.07, 26.3724, 0.0263724),
(178, 'Lipa', 2021, 'Q4', 'November', 'biodegradable', 'BiodegradableFood Waste', 44.32, 27.7829, 0.0277829),
(179, 'Lipa', 2021, 'Q4', 'December', 'biodegradable', 'BiodegradableFood Waste', 84.77, 53.1398, 0.0531398),
(180, 'Lipa', 2021, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 183.41, 114.974, 0.114974),
(181, 'Lipa', 2021, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 481.49, 301.832, 0.301832),
(182, 'Lipa', 2021, 'Q1', 'March', 'biodegradable', 'BiodegradableFood Waste', 426.88, 267.598, 0.267598),
(183, 'Lipa', 2021, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 332.53, 208.453, 0.208453),
(184, 'Lipa', 2021, 'Q2', 'May', 'residual', 'ResidualResidual', 524.26, 233.946, 0.233946),
(185, 'Lipa', 2021, 'Q2', 'June', 'residual', 'ResidualResidual', 130.44, 58.2075, 0.0582075),
(186, 'Lipa', 2021, 'Q3', 'July', 'residual', 'ResidualResidual', 222.23, 99.1679, 0.0991679),
(187, 'Lipa', 2021, 'Q3', 'August', 'residual', 'ResidualResidual', 342.27, 152.735, 0.152735),
(188, 'Lipa', 2021, 'Q3', 'September', 'residual', 'ResidualResidual', 222.39, 99.2393, 0.0992393),
(189, 'Lipa', 2021, 'Q4', 'October', 'residual', 'ResidualResidual', 199.36, 88.9624, 0.0889624),
(190, 'Lipa', 2021, 'Q4', 'November', 'residual', 'ResidualResidual', 353.31, 157.661, 0.157661),
(191, 'Lipa', 2021, 'Q4', 'December', 'residual', 'ResidualResidual', 283.85, 126.665, 0.126665),
(192, 'Lipa', 2021, 'Q1', 'January', 'recyclable', 'RecyclableMixed Plastic', 22.66, 0.201674, 0.000201674),
(193, 'Lipa', 2021, 'Q1', 'February', 'recyclable', 'RecyclableMixed Plastic', 31.11, 0.276879, 0.000276879),
(194, 'Lipa', 2021, 'Q1', 'March', 'recyclable', 'RecyclableMixed Plastic', 14.39, 0.128071, 0.000128071),
(195, 'Lipa', 2021, 'Q2', 'April', 'recyclable', 'RecyclableMixed Plastic', 13.5, 0.12015, 0.00012015),
(196, 'Lipa', 2021, 'Q2', 'May', 'recyclable', 'RecyclableMixed Plastic', 12.67, 0.112763, 0.000112763),
(197, 'Lipa', 2021, 'Q2', 'June', 'recyclable', 'RecyclableMixed Plastic', 2.33, 0.020737, 0.000020737),
(198, 'Lipa', 2021, 'Q3', 'July', 'recyclable', 'RecyclableMixed Plastic', 2.13, 0.018957, 0.000018957),
(199, 'Lipa', 2021, 'Q3', 'August', 'recyclable', 'RecyclableMixed Plastic', 3.86, 0.034354, 0.000034354),
(200, 'Lipa', 2021, 'Q3', 'September', 'recyclable', 'RecyclableMixed Plastic', 2.07, 0.018423, 0.000018423),
(201, 'Lipa', 2021, 'Q4', 'October', 'recyclable', 'RecyclableMixed Plastic', 2.03, 0.018067, 0.000018067),
(202, 'Lipa', 2021, 'Q4', 'November', 'recyclable', 'RecyclableMixed Plastic', 4.85, 0.043165, 0.000043165),
(203, 'Lipa', 2021, 'Q4', 'December', 'recyclable', 'RecyclableMixed Plastic', 2.53, 0.022517, 0.000022517),
(204, 'Lipa', 2020, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 454.68, 285.025, 0.285025),
(205, 'Lipa', 2020, 'Q1', 'February', 'biodegradable', 'BiodegradableFood Waste', 183.27, 114.886, 0.114886),
(206, 'Lipa', 2020, 'Q1', 'March', 'biodegradable', 'BiodegradableFood Waste', 87.32, 54.7383, 0.0547383),
(207, 'Lipa', 2020, 'Q2', 'April', 'biodegradable', 'BiodegradableFood Waste', 98.61, 61.8157, 0.0618156),
(208, 'Lipa', 2020, 'Q2', 'May', 'biodegradable', 'BiodegradableFood Waste', 290.86, 182.331, 0.182331),
(209, 'Lipa', 2020, 'Q2', 'June', 'biodegradable', 'BiodegradableFood Waste', 52.16, 32.6975, 0.0326975),
(210, 'Lipa', 2020, 'Q3', 'July', 'biodegradable', 'BiodegradableFood Waste', 107.73, 67.5327, 0.0675327),
(211, 'Lipa', 2020, 'Q3', 'August', 'biodegradable', 'BiodegradableFood Waste', 119.88, 75.1492, 0.0751492),
(212, 'Lipa', 2020, 'Q3', 'September', 'biodegradable', 'BiodegradableFood Waste', 67.24, 42.1507, 0.0421507),
(213, 'Lipa', 2020, 'Q4', 'October', 'biodegradable', 'BiodegradableFood Waste', 42.64, 26.7297, 0.0267297),
(214, 'Lipa', 2020, 'Q4', 'November', 'biodegradable', 'BiodegradableFood Waste', 52.47, 32.8919, 0.0328919),
(215, 'Lipa', 2020, 'Q4', 'December', 'biodegradable', 'BiodegradableFood Waste', 84.12, 52.7323, 0.0527323),
(216, 'Lipa', 2020, 'Q1', 'January', 'residual', 'ResidualResidual', 194, 86.5706, 0.0865706),
(217, 'Lipa', 2020, 'Q1', 'February', 'residual', 'ResidualResidual', 470.39, 209.907, 0.209907),
(218, 'Lipa', 2020, 'Q1', 'March', 'residual', 'ResidualResidual', 405.04, 180.745, 0.180745),
(219, 'Lipa', 2020, 'Q2', 'April', 'residual', 'ResidualResidual', 315.32, 140.708, 0.140708),
(220, 'Lipa', 2020, 'Q2', 'May', 'residual', 'ResidualResidual', 448.91, 200.322, 0.200322),
(221, 'Lipa', 2020, 'Q2', 'June', 'residual', 'ResidualResidual', 135.46, 60.4477, 0.0604477),
(222, 'Lipa', 2020, 'Q3', 'July', 'residual', 'ResidualResidual', 208.08, 92.8536, 0.0928536),
(223, 'Lipa', 2020, 'Q3', 'August', 'residual', 'ResidualResidual', 329.69, 147.121, 0.147121),
(224, 'Lipa', 2020, 'Q3', 'September', 'residual', 'ResidualResidual', 198.72, 88.6768, 0.0886768),
(225, 'Lipa', 2020, 'Q4', 'October', 'recyclable', 'RecyclableMixed Plastic', 194.13, 1.72776, 0.00172776),
(226, 'Lipa', 2020, 'Q4', 'November', 'residual', 'ResidualResidual', 354.08, 158.005, 0.158005),
(227, 'Lipa', 2020, 'Q4', 'December', 'residual', 'ResidualResidual', 276.77, 123.506, 0.123506),
(228, 'Lipa', 2020, 'Q1', 'January', 'recyclable', 'RecyclableMixed Plastic', 25.85, 0.230065, 0.000230065),
(229, 'Lipa', 2020, 'Q1', 'February', 'recyclable', 'RecyclableMixed Plastic', 32.49, 0.289161, 0.000289161),
(230, 'Lipa', 2020, 'Q1', 'March', 'recyclable', 'RecyclableMixed Plastic', 14.64, 0.130296, 0.000130296),
(231, 'Lipa', 2020, 'Q2', 'April', 'recyclable', 'RecyclableMixed Plastic', 14.59, 0.129851, 0.000129851),
(232, 'Lipa', 2020, 'Q2', 'May', 'recyclable', 'RecyclableMixed Plastic', 14.95, 0.133055, 0.000133055),
(233, 'Lipa', 2020, 'Q2', 'June', 'recyclable', 'RecyclableMixed Plastic', 2.37, 0.021093, 0.000021093),
(234, 'Lipa', 2020, 'Q3', 'July', 'recyclable', 'RecyclableMixed Plastic', 1.96, 0.017444, 0.000017444),
(235, 'Lipa', 2020, 'Q3', 'August', 'recyclable', 'RecyclableMixed Plastic', 3.86, 0.034354, 0.000034354),
(236, 'Lipa', 2020, 'Q3', 'September', 'recyclable', 'RecyclableMixed Plastic', 2.39, 0.021271, 0.000021271),
(237, 'Lipa', 2020, 'Q4', 'October', 'recyclable', 'RecyclableMixed Plastic', 5.84, 0.051976, 0.000051976),
(238, 'Lipa', 2020, 'Q4', 'November', 'recyclable', 'RecyclableMixed Plastic', 4.4, 0.03916, 0.00003916),
(239, 'Lipa', 2020, 'Q4', 'December', 'recyclable', 'RecyclableMixed Plastic', 2.59, 0.023051, 0.000023051),
(240, 'Lipa', 2024, 'Q4', 'November', 'Biodegradable', 'BiodegradableFood Waste', 150, 0, 0),
(241, 'Lipa', 2023, 'Q2', 'June', 'Recyclable', 'Mixed Plastic', 25, 0.2225, 0.0002225),
(242, 'Lipa', 2024, 'Q4', 'October', 'Biodegradable', 'Food Waste', 15, 9.40305, 0.00940305),
(243, 'Lipa', 2024, 'Q3', 'July', 'Residual', 'Residual Waste', 45, 20.0808, 0.0200808),
(244, 'Lipa', 2024, 'Q3', 'August', 'Residual', 'Residual Waste', 90, 40.1616, 0.0401616),
(245, 'Lipa', 2024, 'Q3', 'September', 'Biodegradable', 'Garden Waste', 200, 115.792, 0.115792);

-- --------------------------------------------------------

--
-- Table structure for table `tblsolidwasteunsegregated`
--

CREATE TABLE `tblsolidwasteunsegregated` (
  `id` int(11) NOT NULL,
  `Campus` char(20) DEFAULT NULL,
  `Year` year(4) DEFAULT NULL,
  `Month` char(20) DEFAULT NULL,
  `WasteType` varchar(30) DEFAULT NULL,
  `QuantityInKG` float DEFAULT NULL,
  `SentToLandfillKG` float DEFAULT NULL,
  `SentToLandfillTONS` float DEFAULT NULL,
  `Percentage` float DEFAULT NULL,
  `GHGEmissionKGCO2e` float DEFAULT NULL,
  `GHGEmissionTCO2e` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblsolidwasteunsegregated`
--

INSERT INTO `tblsolidwasteunsegregated` (`id`, `Campus`, `Year`, `Month`, `WasteType`, `QuantityInKG`, `SentToLandfillKG`, `SentToLandfillTONS`, `Percentage`, `GHGEmissionKGCO2e`, `GHGEmissionTCO2e`) VALUES
(61, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(62, 'Lipa', '2021', 'February', 'Mixed Municipal Solid Waste', 300, 40, 0.04, 13.3333, 2.66, 0.00266),
(63, 'Lipa', '2020', 'January', 'Mixed Municipal Solid Waste', 600, 150, 0.15, 25, 9.975, 0.009975),
(64, 'Lipa', '2020', 'February', 'Mixed Municipal Solid Waste', 670, 300, 0.3, 44.7761, 19.95, 0.01995),
(65, 'Lipa', '2020', 'March', 'Mixed Municipal Solid Waste', 150, 30, 0.03, 20, 1.995, 0.001995),
(66, 'Lipa', '2020', 'April', 'Mixed Municipal Solid Waste', 700, 370, 0.37, 52.8571, 24.605, 0.024605),
(67, 'Lipa', '2020', 'May', 'Mixed Municipal Solid Waste', 500, 200, 0.2, 40, 13.3, 0.0133),
(68, 'Lipa', '2020', 'June', 'Mixed Municipal Solid Waste', 800, 500, 0.5, 62.5, 33.25, 0.03325),
(69, 'Lipa', '2020', 'July', 'Mixed Municipal Solid Waste', 700, 300, 0.3, 42.8571, 19.95, 0.01995),
(70, 'Lipa', '2020', 'August', 'Mixed Municipal Solid Waste', 500, 400, 0.4, 80, 26.6, 0.0266),
(72, 'Lipa', '2020', 'September', 'Mixed Municipal Solid Waste', 800, 450, 0.45, 56.25, 29.925, 0.029925),
(74, 'Lipa', '2020', 'October', 'Mixed Municipal Solid Waste', 780, 230, 0.23, 29.4872, 15.295, 0.015295),
(75, 'Lipa', '2020', 'November', 'Mixed Municipal Solid Waste', 789, 560, 0.56, 70.9759, 37.24, 0.03724),
(76, 'Lipa', '2020', 'December', 'Mixed Municipal Solid Waste', 890, 600, 0.6, 67.4157, 39.9, 0.0399),
(77, 'Lipa', '2021', 'March', 'Mixed Municipal Solid Waste', 780, 450, 0.45, 57.6923, 29.925, 0.029925),
(78, 'Lipa', '2021', 'April', 'Mixed Municipal Solid Waste', 550, 320, 0.32, 58.1818, 21.28, 0.02128),
(79, 'Lipa', '2021', 'May', 'Mixed Municipal Solid Waste', 670, 320, 0.32, 47.7612, 21.28, 0.02128),
(80, 'Lipa', '2021', 'June', 'Mixed Municipal Solid Waste', 345, 210, 0.21, 60.8696, 13.965, 0.013965),
(81, 'Lipa', '2021', 'July', 'Mixed Municipal Solid Waste', 900, 560, 0.56, 62.2222, 37.24, 0.03724),
(82, 'Lipa', '2021', 'August', 'Mixed Municipal Solid Waste', 1090, 890, 0.89, 81.6514, 59.185, 0.059185),
(83, 'Lipa', '2021', 'September', 'Mixed Municipal Solid Waste', 560, 490, 0.49, 87.5, 32.585, 0.032585),
(84, 'Lipa', '2021', 'October', 'Mixed Municipal Solid Waste', 680, 300, 0.3, 44.1176, 19.95, 0.01995),
(85, 'Lipa', '2021', 'November', 'Mixed Municipal Solid Waste', 540, 290, 0.29, 53.7037, 19.285, 0.019285),
(86, 'Lipa', '2021', 'December', 'Mixed Municipal Solid Waste', 780, 510, 0.51, 65.3846, 33.915, 0.033915),
(87, 'Lipa', '2022', 'January', 'Mixed Municipal Solid Waste', 100, 56, 0.056, 56, 3.724, 0.003724),
(88, 'Lipa', '2022', 'February', 'Mixed Municipal Solid Waste', 678, 321, 0.321, 47.3451, 21.3465, 0.0213465),
(89, 'Lipa', '2022', 'March', 'Mixed Municipal Solid Waste', 670, 432, 0.432, 64.4776, 28.728, 0.028728),
(90, 'Lipa', '2022', 'April', 'Mixed Municipal Solid Waste', 894, 670, 0.67, 74.9441, 44.555, 0.044555),
(91, 'Lipa', '2022', 'May', 'Mixed Municipal Solid Waste', 789, 234, 0.234, 29.6578, 15.561, 0.015561),
(92, 'Lipa', '2022', 'June', 'Mixed Municipal Solid Waste', 672, 459, 0.459, 68.3036, 30.5235, 0.0305235),
(93, 'Lipa', '2022', 'July', 'Mixed Municipal Solid Waste', 1230, 780, 0.78, 63.4146, 51.87, 0.05187),
(94, 'Lipa', '2022', 'August', 'Mixed Municipal Solid Waste', 782, 123, 0.123, 15.7289, 8.1795, 0.0081795),
(95, 'Lipa', '2022', 'September', 'Mixed Municipal Solid Waste', 451, 340, 0.34, 75.388, 22.61, 0.02261),
(96, 'Lipa', '2022', 'October', 'Mixed Municipal Solid Waste', 745, 458, 0.458, 61.4765, 30.457, 0.030457),
(97, 'Lipa', '2022', 'November', 'Mixed Municipal Solid Waste', 1500, 830, 0.83, 55.3333, 55.195, 0.055195),
(98, 'Lipa', '2022', 'December', 'Mixed Municipal Solid Waste', 900, 780, 0.78, 86.6667, 51.87, 0.05187),
(99, 'Lipa', '2023', 'January', 'Mixed Municipal Solid Waste', 569, 221, 0.221, 38.8401, 14.6965, 0.0146965),
(100, 'Lipa', '2023', 'February', 'Mixed Municipal Solid Waste', 893, 445, 0.445, 49.832, 29.5925, 0.0295925),
(101, 'Lipa', '2023', 'March', 'Mixed Municipal Solid Waste', 678, 165, 0.165, 24.3363, 10.9725, 0.0109725),
(102, 'Lipa', '2023', 'April', 'Mixed Municipal Solid Waste', 780, 458, 0.458, 58.7179, 30.457, 0.030457),
(103, 'Lipa', '2023', 'May', 'Mixed Municipal Solid Waste', 902, 560, 0.56, 62.0843, 37.24, 0.03724),
(104, 'Lipa', '2023', 'June', 'Mixed Municipal Solid Waste', 781, 435, 0.435, 55.6978, 28.9275, 0.0289275),
(105, 'Lipa', '2023', 'July', 'Mixed Municipal Solid Waste', 380, 125, 0.125, 32.8947, 8.3125, 0.0083125),
(106, 'Lipa', '2023', 'August', 'Mixed Municipal Solid Waste', 895, 870, 0.87, 97.2067, 57.855, 0.057855),
(107, 'Lipa', '2023', 'September', 'Mixed Municipal Solid Waste', 865, 377, 0.377, 43.5838, 25.0705, 0.0250705),
(108, 'Lipa', '2023', 'October', 'Mixed Municipal Solid Waste', 535, 220, 0.22, 41.1215, 14.63, 0.01463),
(109, 'Lipa', '2023', 'November', 'Mixed Municipal Solid Waste', 1000, 590, 0.59, 59, 39.235, 0.039235),
(110, 'Lipa', '2023', 'December', 'Mixed Municipal Solid Waste', 3450, 2390, 2.39, 69.2754, 158.935, 0.158935),
(111, 'Lipa', '2024', 'January', 'Mixed Municipal Solid Waste', 780, 346, 0.346, 44.359, 23.009, 0.023009),
(112, 'Lipa', '2024', 'February', 'Mixed Municipal Solid Waste', 345, 230, 0.23, 66.6667, 15.295, 0.015295),
(113, 'Lipa', '2024', 'March', 'Mixed Municipal Solid Waste', 910, 770, 0.77, 84.6154, 51.205, 0.051205),
(114, 'Lipa', '2024', 'April', 'Mixed Municipal Solid Waste', 800, 790, 0.79, 98.75, 52.535, 0.052535),
(115, 'Lipa', '2024', 'May', 'Mixed Municipal Solid Waste', 799, 538, 0.538, 67.3342, 35.777, 0.035777),
(116, 'Lipa', '2024', 'June', 'Mixed Municipal Solid Waste', 234, 98, 0.098, 41.8803, 6.517, 0.006517),
(117, 'Lobo', '2023', 'November', 'Mixed Municipal Solid Waste', 3, 23, 0.023, 766.667, 1.5295, 0.0015295),
(118, 'Lipa', '2020', 'January', 'Mixed Municipal Solid Waste', 34, 45, 0.045, 132.353, 2.9925, 0.0029925),
(119, 'Lipa', '2024', 'July', 'Mixed Municipal Solid Waste', 56, 78, 0.078, 139.286, 5.187, 0.005187),
(120, 'Lipa', '2024', 'August', 'Mixed Municipal Solid Waste', 67, 90, 0.09, 134.328, 5.985, 0.005985),
(121, 'Lipa', '2024', 'September', 'Mixed Municipal Solid Waste', 90, 100, 0.1, 111.111, 6.65, 0.00665),
(122, 'Lipa', '2024', 'October', 'Mixed Municipal Solid Waste', 350, 450, 0.45, 128.571, 29.925, 0.029925),
(123, 'Lipa', '2019', 'January', 'Mixed Municipal Solid Waste', 34, 56, 0.056, 164.706, 3.724, 0.003724),
(124, 'Lipa', '2019', 'February', 'Mixed Municipal Solid Waste', 42, 78, 0.078, 185.714, 5.187, 0.005187),
(125, 'Lipa', '2019', 'March', 'Mixed Municipal Solid Waste', 67, 105, 0.105, 156.716, 6.9825, 0.0069825),
(126, 'Lipa', '2019', 'April', 'Mixed Municipal Solid Waste', 56, 89, 0.089, 158.929, 5.9185, 0.0059185),
(127, 'Lobo', '2019', 'May', 'Mixed Municipal Solid Waste', 78, 123, 0.123, 157.692, 8.1795, 0.0081795),
(128, 'Lipa', '2019', 'June', 'Mixed Municipal Solid Waste', 67, 109, 0.109, 162.687, 7.2485, 0.0072485),
(129, 'Lipa', '2019', 'July', 'Mixed Municipal Solid Waste', 89, 123, 0.123, 138.202, 8.1795, 0.0081795),
(131, 'Lipa', '2019', 'August', 'Mixed Municipal Solid Waste', 67, 88, 0.088, 131.343, 5.852, 0.005852),
(132, 'Lipa', '2019', 'September', 'Mixed Municipal Solid Waste', 98, 102, 0.102, 104.082, 6.783, 0.006783),
(133, 'Lipa', '2019', 'October', 'Mixed Municipal Solid Waste', 108, 104, 0.104, 96.2963, 6.916, 0.006916),
(134, 'Lipa', '2019', 'November', 'Mixed Municipal Solid Waste', 90, 190, 0.19, 211.111, 12.635, 0.012635),
(135, 'Lipa', '2019', 'December', 'Mixed Municipal Solid Waste', 56, 21, 0.021, 37.5, 1.3965, 0.0013965);

-- --------------------------------------------------------

--
-- Table structure for table `tbltreatedwater`
--

CREATE TABLE `tbltreatedwater` (
  `id` int(11) NOT NULL,
  `Campus` varchar(255) DEFAULT NULL,
  `Month` varchar(50) DEFAULT NULL,
  `TreatedWaterVolume` float(10,2) DEFAULT NULL,
  `ReusedTreatedWaterVolume` decimal(10,2) DEFAULT NULL,
  `EffluentVolume` decimal(10,2) DEFAULT NULL,
  `PricePerLiter` decimal(10,2) DEFAULT NULL,
  `FactorKGCO2e` decimal(10,5) DEFAULT NULL,
  `FactorTCO2e` decimal(10,5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbltreatedwater`
--

INSERT INTO `tbltreatedwater` (`id`, `Campus`, `Month`, `TreatedWaterVolume`, `ReusedTreatedWaterVolume`, `EffluentVolume`, `PricePerLiter`, `FactorKGCO2e`, `FactorTCO2e`) VALUES
(131, 'Lipa', 'January', 3000.00, 800.00, 2200.00, 598.40, 598.40000, 0.59840),
(132, 'Lipa', 'March', 500.00, 200.00, 300.00, 81.60, 81.60000, 0.08160),
(133, 'Lipa', 'February', 1200.00, 300.00, 900.00, 244.80, 244.80000, 0.24480),
(134, 'Lipa', 'April', 2000.00, 500.00, 1500.00, 408.00, 408.00000, 0.40800),
(135, 'Lipa', 'May', 600.00, 300.00, 300.00, 81.60, 81.60000, 0.08160),
(136, 'Lipa', 'June', 700.00, 400.00, 300.00, 81.60, 81.60000, 0.08160),
(137, 'Lipa', 'July', 500.00, 100.00, 400.00, 108.80, 108.80000, 0.10880),
(138, 'Lipa', 'August', 340.00, 150.00, 190.00, 51.68, 51.68000, 0.05168),
(139, 'Lipa', 'September', 700.00, 450.00, 250.00, 68.00, 68.00000, 0.06800),
(140, 'Lipa', 'October', 9807.00, 670.00, 9137.00, 2485.26, 2485.26400, 2.48526),
(141, 'Lipa', 'November', 560.00, 490.00, 70.00, 19.04, 19.04000, 0.01904),
(142, 'Lipa', 'December', 780.00, 560.00, 220.00, 59.84, 59.84000, 0.05984),
(143, 'Lipa', 'January', 780.00, 450.00, 330.00, 89.76, 89.76000, 0.08976),
(144, 'Lipa', 'February', 5609.00, 1560.00, 4049.00, 1101.33, 1101.32800, 1.10133),
(145, 'Lipa', 'March', 890.00, 300.00, 590.00, 160.48, 160.48000, 0.16048),
(146, 'Lipa', 'April', 500.00, 350.00, 150.00, 40.80, 40.80000, 0.04080),
(147, 'Lipa', 'May', 2300.00, 1000.00, 1300.00, 353.60, 353.60000, 0.35360),
(148, 'Lipa', 'June', 670.00, 500.00, 170.00, 46.24, 46.24000, 0.04624),
(149, 'Lipa', 'July', 1500.00, 600.00, 900.00, 244.80, 244.80000, 0.24480),
(150, 'Lipa', 'August', 800.00, 560.00, 240.00, 65.28, 65.28000, 0.06528),
(151, 'Lipa', 'September', 890.00, 670.00, 220.00, 59.84, 59.84000, 0.05984),
(152, 'Lipa', 'October', 780.00, 450.00, 330.00, 89.76, 89.76000, 0.08976),
(153, 'Lipa', 'November', 560.00, 310.00, 250.00, 68.00, 68.00000, 0.06800),
(154, 'Lipa', 'December', 670.00, 320.00, 350.00, 95.20, 95.20000, 0.09520),
(155, 'Lipa', 'January', 560.00, 130.00, 430.00, 116.96, 116.96000, 0.11696),
(156, 'Lipa', 'February', 840.00, 355.00, 485.00, 131.92, 131.92000, 0.13192),
(157, 'Lipa', 'March', 600.00, 200.00, 400.00, 108.80, 108.80000, 0.10880),
(158, 'Lipa', 'April', 700.00, 100.00, 600.00, 163.20, 163.20000, 0.16320),
(159, 'Lipa', 'May', 1660.00, 1200.00, 460.00, 125.12, 125.12000, 0.12512),
(160, 'Lipa', 'June', 5700.00, 3450.00, 2250.00, 612.00, 612.00000, 0.61200),
(161, 'Lipa', 'July', 670.00, 467.00, 203.00, 55.22, 55.21600, 0.05522),
(162, 'Lipa', 'August', 890.00, 566.00, 324.00, 88.13, 88.12800, 0.08813),
(163, 'Lipa', 'September', 780.00, 342.00, 438.00, 119.14, 119.13600, 0.11914),
(164, 'Lipa', 'October', 200.00, 45.00, 155.00, 42.16, 42.16000, 0.04216),
(165, 'Lipa', 'November', 683.00, 331.00, 352.00, 95.74, 95.74400, 0.09574),
(166, 'Lipa', 'December', 777.00, 222.00, 555.00, 150.96, 150.96000, 0.15096),
(167, 'Lipa', 'January', 789.00, 300.00, 489.00, 133.01, 133.00800, 0.13301),
(168, 'Lipa', 'February', 1222.00, 560.00, 662.00, 180.06, 180.06400, 0.18006),
(169, 'Lipa', 'March', 800.00, 450.00, 350.00, 95.20, 95.20000, 0.09520),
(170, 'Lipa', 'April', 810.00, 230.00, 580.00, 157.76, 157.76000, 0.15776),
(171, 'Lipa', 'May', 540.00, 110.00, 430.00, 116.96, 116.96000, 0.11696),
(172, 'Lipa', 'June', 510.00, 220.00, 290.00, 78.88, 78.88000, 0.07888),
(173, 'Lipa', 'July', 600.00, 100.00, 500.00, 136.00, 136.00000, 0.13600),
(174, 'Lipa', 'August', 1220.00, 345.00, 875.00, 238.00, 238.00000, 0.23800),
(175, 'Lipa', 'September', 567.00, 234.00, 333.00, 90.58, 90.57600, 0.09058),
(176, 'Lipa', 'October', 567.00, 98.00, 469.00, 127.57, 127.56800, 0.12757),
(177, 'Lipa', 'November', 670.00, 210.00, 460.00, 125.12, 125.12000, 0.12512),
(178, 'Lipa', 'December', 230.00, 60.00, 170.00, 46.24, 46.24000, 0.04624),
(179, 'Lipa', 'January', 560.00, 333.00, 227.00, 61.74, 61.74400, 0.06174),
(180, 'Lipa', 'February', 670.00, 130.00, 540.00, 146.88, 146.88000, 0.14688),
(181, 'Lipa', 'March', 9876.00, 5679.00, 4197.00, 1141.58, 1141.58400, 1.14158),
(182, 'Lipa', 'April', 4678.00, 1239.00, 3439.00, 935.41, 935.40800, 0.93541),
(183, 'Lipa', 'May', 789.00, 321.00, 468.00, 127.30, 127.29600, 0.12730),
(184, 'Lipa', 'June', 567.00, 230.00, 337.00, 91.66, 91.66400, 0.09166),
(190, 'Lipa', 'January', 56.00, 123.00, -67.00, -18.22, -18.22400, -0.01822),
(191, 'Lipa', 'February', 43.00, 565.00, -522.00, -141.98, -141.98400, -0.14198),
(192, 'Lipa', 'May', 56.00, 43.00, 13.00, 3.54, 3.53600, 0.00354),
(193, 'Lipa', 'May', 454.00, 32.00, 422.00, 114.78, 114.78400, 0.11478),
(194, 'Lipa', 'June', 453.00, 43.00, 410.00, 111.52, 111.52000, 0.11152),
(195, 'Lipa', 'July', 452.00, 89.00, 363.00, 98.74, 98.73600, 0.09874),
(196, 'Lipa', 'August', 567.00, 211.00, 356.00, 96.83, 96.83200, 0.09683),
(197, 'Lipa', 'September', 456.00, 4332.00, -3876.00, -1054.27, -1054.27200, -1.05427),
(198, 'Lipa', 'October', 32.00, 78.00, -46.00, -12.51, -12.51200, -0.01251),
(199, 'Lipa', 'October', 445.00, 332.00, 113.00, 30.74, 30.73600, 0.03074),
(200, 'Lipa', 'November', 311.00, 456.00, -145.00, -39.44, -39.44000, -0.03944),
(201, 'Lipa', 'December', 4456.00, 422.00, 4034.00, 1097.25, 1097.24800, 1.09725);

-- --------------------------------------------------------

--
-- Table structure for table `tblwater`
--

CREATE TABLE `tblwater` (
  `id` int(11) NOT NULL,
  `Campus` varchar(255) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Category` varchar(255) DEFAULT NULL,
  `PreviousReading` decimal(10,2) DEFAULT NULL,
  `CurrentReading` decimal(10,2) DEFAULT NULL,
  `Consumption` float(10,2) DEFAULT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `PricePerLiter` decimal(10,2) DEFAULT NULL,
  `FactorKGCO2e` decimal(10,5) DEFAULT NULL,
  `FactorTCO2e` decimal(10,5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblwater`
--

INSERT INTO `tblwater` (`id`, `Campus`, `Date`, `Category`, `PreviousReading`, `CurrentReading`, `Consumption`, `TotalAmount`, `PricePerLiter`, `FactorKGCO2e`, `FactorTCO2e`) VALUES
(10, 'Lipa', '2020-01-27', 'Mains', 5221.00, 5259.00, 38.00, 1034.00, 27.21, 0.56620, 0.00057),
(11, 'Lipa', '2020-01-28', 'Mains', 5110.00, 5134.00, 24.00, 1080.00, 45.00, 0.35760, 0.00036),
(12, 'Lipa', '2020-01-29', 'Drinking Water', 5230.00, 5268.00, 38.00, 1045.00, 27.50, 0.56620, 0.00057),
(13, 'Lipa', '2020-02-28', 'Mains', 5259.00, 5283.00, 24.00, 908.00, 37.83, 0.35760, 0.00036),
(14, 'Lipa', '2020-02-27', 'Mains', 5134.00, 5166.00, 32.00, 1378.00, 43.06, 0.47680, 0.00048),
(15, 'Lipa', '2020-02-28', 'Drinking Water', 5268.00, 5290.00, 22.00, 805.00, 36.59, 0.32780, 0.00033),
(16, 'Lipa', '2020-03-31', 'Mains', 5283.00, 5420.00, 137.00, 3098.00, 22.61, 2.04130, 0.00204),
(17, 'Lipa', '2020-03-28', 'Mains', 5166.00, 5320.00, 154.00, 3450.00, 22.40, 2.29460, 0.00229),
(18, 'Lipa', '2020-03-30', 'Drinking Water', 5290.00, 5392.00, 102.00, 3102.00, 30.41, 1.51980, 0.00152),
(19, 'Lipa', '2020-04-28', 'Mains', 5420.00, 5601.00, 181.00, 3896.00, 21.52, 2.69690, 0.00270),
(20, 'Lipa', '2020-04-29', 'Mains', 5320.00, 5439.00, 119.00, 3450.00, 28.99, 1.77310, 0.00177),
(21, 'Lipa', '2020-04-29', 'Drinking Water', 5439.00, 5549.00, 110.00, 2970.00, 27.00, 1.63900, 0.00164),
(22, 'Lipa', '2020-05-24', 'Mains', 5601.00, 5699.00, 98.00, 2880.00, 29.39, 1.46020, 0.00146),
(23, 'Lipa', '2020-05-29', 'Mains', 5439.00, 5531.00, 92.00, 2802.00, 30.46, 1.37080, 0.00137),
(24, 'Lipa', '2020-05-30', 'Drinking Water', 5549.00, 5653.00, 104.00, 3009.00, 28.93, 1.54960, 0.00155),
(25, 'Lipa', '2020-06-29', 'Mains', 5699.00, 5752.00, 53.00, 1980.00, 37.36, 0.78970, 0.00079),
(26, 'Lipa', '2020-06-30', 'Mains', 5531.00, 5596.00, 65.00, 1990.00, 30.62, 0.96850, 0.00097),
(27, 'Lipa', '2020-06-29', 'Drinking Water', 5653.00, 5699.00, 46.00, 1500.00, 32.61, 0.68540, 0.00069),
(28, 'Lipa', '2020-07-30', 'Mains', 5752.00, 5791.00, 39.00, 1209.00, 31.00, 0.58110, 0.00058),
(29, 'Lipa', '2020-07-30', 'Mains', 5596.00, 5659.00, 63.00, 1606.00, 25.49, 0.93870, 0.00094),
(30, 'Lipa', '2020-07-30', 'Drinking Water', 5699.00, 5763.00, 64.00, 1890.00, 29.53, 0.95360, 0.00095),
(31, 'Lipa', '2020-08-30', 'Mains', 5791.00, 5839.00, 48.00, 1506.00, 31.38, 0.71520, 0.00072),
(32, 'Lipa', '2020-08-31', 'Mains', 5659.00, 5692.00, 33.00, 1330.00, 40.30, 0.49170, 0.00049),
(33, 'Lipa', '2020-08-31', 'Drinking Water', 5763.00, 5801.00, 38.00, 1503.00, 39.55, 0.56620, 0.00057),
(34, 'Lipa', '2020-09-29', 'Mains', 5839.00, 5909.00, 70.00, 2202.00, 31.46, 1.04300, 0.00104),
(35, 'Lipa', '2020-09-30', 'Mains', 5692.00, 5759.00, 67.00, 2009.00, 29.99, 0.99830, 0.00100),
(36, 'Lipa', '2020-09-30', 'Drinking Water', 5801.00, 5849.00, 48.00, 1250.00, 26.04, 0.71520, 0.00072),
(37, 'Lipa', '2020-10-30', 'Mains', 5909.00, 5963.00, 54.00, 1600.00, 29.63, 0.80460, 0.00080),
(38, 'Lipa', '2020-10-30', 'Mains', 5759.00, 5796.00, 37.00, 950.00, 25.68, 0.55130, 0.00055),
(39, 'Lipa', '2020-10-30', 'Drinking Water', 5849.00, 5889.00, 40.00, 1109.00, 27.73, 0.59600, 0.00060),
(40, 'Lipa', '2020-11-30', 'Mains', 5963.00, 6039.00, 76.00, 2780.00, 36.58, 1.13240, 0.00113),
(41, 'Lipa', '2020-11-30', 'Mains', 5796.00, 5863.00, 67.00, 2330.00, 34.78, 0.99830, 0.00100),
(42, 'Lipa', '2020-11-29', 'Drinking Water', 5889.00, 5946.00, 57.00, 1890.00, 33.16, 0.84930, 0.00085),
(43, 'Lipa', '2020-12-30', 'Mains', 6039.00, 6125.00, 86.00, 2560.00, 29.77, 1.28140, 0.00128),
(44, 'Lipa', '2020-12-31', 'Mains', 5863.00, 5916.00, 53.00, 1900.00, 35.85, 0.78970, 0.00079),
(45, 'Lipa', '2020-12-31', 'Drinking Water', 5949.00, 6012.00, 63.00, 2009.00, 31.89, 0.93870, 0.00094),
(46, 'Lipa', '2021-01-30', 'Mains', 6125.00, 6185.00, 60.00, 1600.00, 26.67, 0.89400, 0.00089),
(47, 'Lipa', '2021-01-30', 'Mains', 5916.00, 5993.00, 77.00, 2200.00, 28.57, 1.14730, 0.00115),
(48, 'Lipa', '2021-01-31', 'Drinking Water', 6012.00, 6086.00, 74.00, 2100.00, 28.38, 1.10260, 0.00110),
(49, 'Lipa', '2021-02-28', 'Mains', 6185.00, 6224.00, 39.00, 890.00, 22.82, 0.58110, 0.00058),
(50, 'Lipa', '2021-02-28', 'Mains', 5993.00, 6086.00, 93.00, 2990.00, 32.15, 1.38570, 0.00139),
(51, 'Lipa', '2021-02-28', 'Drinking Water', 6086.00, 6149.00, 63.00, 1880.00, 29.84, 0.93870, 0.00094),
(53, 'Lipa', '2021-03-30', 'Mains', 6224.00, 6399.00, 175.00, 3789.00, 21.65, 2.60750, 0.00261),
(54, 'Lipa', '2021-03-31', 'Mains', 6086.00, 6276.00, 190.00, 4009.00, 21.10, 2.83100, 0.00283),
(55, 'Lipa', '2021-03-30', 'Drinking Water', 6149.00, 6286.00, 137.00, 3780.00, 27.59, 2.04130, 0.00204),
(56, 'Lipa', '2021-04-30', 'Mains', 6399.00, 6499.00, 100.00, 2000.00, 20.00, 1.49000, 0.00149),
(57, 'Lipa', '2021-04-11', 'Mains', 6276.00, 6398.00, 122.00, 3700.00, 30.33, 1.81780, 0.00182),
(58, 'Lipa', '2021-04-30', 'Drinking Water', 6286.00, 6388.00, 102.00, 2500.00, 24.51, 1.51980, 0.00152),
(59, 'Lipa', '2021-05-31', 'Mains', 6499.00, 6586.00, 87.00, 2690.00, 30.92, 1.29630, 0.00130),
(60, 'Lipa', '2021-05-31', 'Mains', 6398.00, 6499.00, 101.00, 3000.00, 29.70, 1.50490, 0.00150),
(61, 'Lipa', '2021-05-31', 'Drinking Water', 6388.00, 6498.00, 110.00, 2900.00, 26.36, 1.63900, 0.00164),
(62, 'Lipa', '2021-06-29', 'Mains', 6586.00, 6636.00, 50.00, 1500.00, 30.00, 0.74500, 0.00075),
(63, 'Lipa', '2021-06-30', 'Mains', 6499.00, 6535.00, 36.00, 890.00, 24.72, 0.53640, 0.00054),
(64, 'Lipa', '2021-06-30', 'Drinking Water', 6498.00, 6549.00, 51.00, 1659.00, 32.53, 0.75990, 0.00076),
(65, 'Lipa', '2021-07-30', 'Mains', 6636.00, 6690.00, 54.00, 1450.00, 26.85, 0.80460, 0.00080),
(66, 'Lipa', '2021-07-30', 'Mains', 6535.00, 6585.00, 50.00, 1690.00, 33.80, 0.74500, 0.00075),
(67, 'Lipa', '2021-07-31', 'Drinking Water', 6549.00, 6586.00, 37.00, 1340.00, 36.22, 0.55130, 0.00055),
(68, 'Lipa', '2021-08-31', 'Mains', 6690.00, 6752.00, 63.00, 1990.00, 31.59, 0.93870, 0.00094),
(69, 'Lipa', '2021-08-31', 'Mains', 6585.00, 6646.00, 61.00, 1478.00, 24.23, 0.90890, 0.00091),
(70, 'Lipa', '2021-08-30', 'Drinking Water', 6586.00, 6629.00, 43.00, 1243.00, 28.91, 0.64070, 0.00064),
(71, 'Lipa', '2021-09-30', 'Mains', 6752.00, 6812.00, 60.00, 1670.00, 27.83, 0.89400, 0.00089),
(72, 'Lipa', '2021-09-30', 'Mains', 6646.00, 6682.00, 36.00, 980.00, 27.22, 0.53640, 0.00054),
(73, 'Lipa', '2021-09-30', 'Drinking Water', 6629.00, 6685.00, 56.00, 1600.00, 28.57, 0.83440, 0.00083),
(74, 'Lipa', '2021-10-31', 'Mains', 6812.00, 6846.00, 34.00, 990.00, 29.12, 0.50660, 0.00051),
(75, 'Lipa', '2021-10-31', 'Mains', 6682.00, 6745.00, 63.00, 1670.00, 26.51, 0.93870, 0.00094),
(76, 'Lipa', '2021-10-31', 'Drinking Water', 6685.00, 6734.00, 49.00, 1345.00, 27.45, 0.73010, 0.00073),
(77, 'Lipa', '2021-11-30', 'Mains', 6846.00, 6893.00, 47.00, 1780.00, 37.87, 0.70030, 0.00070),
(78, 'Lipa', '2021-11-30', 'Mains', 6745.00, 6801.00, 56.00, 1600.00, 28.57, 0.83440, 0.00083),
(79, 'Lipa', '2021-11-30', 'Drinking Water', 6734.00, 6791.00, 57.00, 1230.00, 21.58, 0.84930, 0.00085),
(80, 'Lipa', '2021-12-31', 'Mains', 6893.00, 6942.00, 49.00, 1900.00, 38.78, 0.73010, 0.00073),
(81, 'Lipa', '2021-12-31', 'Mains', 6801.00, 6845.00, 44.00, 1789.00, 40.66, 0.65560, 0.00066),
(82, 'Lipa', '2021-12-31', 'Drinking Water', 6791.00, 6859.00, 68.00, 1040.00, 15.29, 1.01320, 0.00101),
(83, 'Lipa', '2022-01-31', 'Mains', 6942.00, 7010.00, 68.00, 1380.00, 20.29, 1.01320, 0.00101),
(84, 'Lipa', '2022-01-31', 'Mains', 6845.00, 6917.00, 72.00, 2056.00, 28.56, 1.07280, 0.00107),
(85, 'Lipa', '2022-01-31', 'Drinking Water', 6859.00, 6925.00, 66.00, 2067.00, 31.32, 0.98340, 0.00098),
(86, 'Lipa', '2022-02-28', 'Mains', 7010.00, 7075.00, 65.00, 1238.00, 19.05, 0.96850, 0.00097),
(87, 'Lipa', '2022-02-28', 'Mains', 6917.00, 6992.00, 75.00, 1560.00, 20.80, 1.11750, 0.00112),
(88, 'Lipa', '2022-02-28', 'Drinking Water', 6925.00, 7010.00, 85.00, 2560.00, 30.12, 1.26650, 0.00127),
(89, 'Lipa', '2022-03-31', 'Mains', 7075.00, 7212.00, 137.00, 3990.00, 29.12, 2.04130, 0.00204),
(90, 'Lipa', '2022-03-31', 'Mains', 6992.00, 7159.00, 167.00, 3900.00, 23.35, 2.48830, 0.00249),
(91, 'Lipa', '2022-03-31', 'Drinking Water', 7010.00, 7146.00, 136.00, 3660.00, 26.91, 2.02640, 0.00203),
(93, 'Lipa', '2022-04-30', 'Mains', 7212.00, 7321.00, 109.00, 3245.00, 29.77, 1.62410, 0.00162),
(94, 'Lipa', '2022-04-30', 'Mains', 7159.00, 7285.00, 126.00, 3670.00, 29.13, 1.87740, 0.00188),
(95, 'Lipa', '2022-04-30', 'Drinking Water', 7146.00, 7266.00, 120.00, 3120.00, 26.00, 1.78800, 0.00179),
(96, 'Lipa', '2022-05-31', 'Mains', 7321.00, 7429.00, 108.00, 3335.00, 30.88, 1.60920, 0.00161),
(97, 'Lipa', '2022-05-31', 'Mains', 7285.00, 7396.00, 111.00, 3400.00, 30.63, 1.65390, 0.00165),
(98, 'Lipa', '2022-05-31', 'Drinking Water', 7266.00, 7391.00, 125.00, 3709.00, 29.67, 1.86250, 0.00186),
(99, 'Lipa', '2022-06-30', 'Mains', 7429.00, 7502.00, 73.00, 2405.00, 32.95, 1.08770, 0.00109),
(100, 'Lipa', '2022-06-30', 'Mains', 7396.00, 7442.00, 46.00, 2089.00, 45.41, 0.68540, 0.00069),
(101, 'Lipa', '2022-06-29', 'Drinking Water', 7391.00, 7467.00, 76.00, 1560.00, 20.53, 1.13240, 0.00113),
(102, 'Lipa', '2022-07-30', 'Mains', 7502.00, 7531.00, 29.00, 590.00, 20.34, 0.43210, 0.00043),
(103, 'Lipa', '2022-07-31', 'Mains', 7442.00, 7487.00, 45.00, 1340.00, 29.78, 0.67050, 0.00067),
(104, 'Lipa', '2022-07-30', 'Drinking Water', 7467.00, 7499.00, 32.00, 1009.00, 31.53, 0.47680, 0.00048),
(105, 'Lipa', '2022-08-29', 'Mains', 7531.00, 7602.00, 71.00, 2006.00, 28.25, 1.05790, 0.00106),
(106, 'Lipa', '2022-08-31', 'Mains', 7487.00, 7569.00, 82.00, 2667.00, 32.52, 1.22180, 0.00122),
(107, 'Lipa', '2022-08-31', 'Drinking Water', 7499.00, 7603.00, 104.00, 2500.00, 24.04, 1.54960, 0.00155),
(108, 'Lipa', '2022-09-30', 'Mains', 7602.00, 7689.00, 87.00, 2560.00, 29.43, 1.29630, 0.00130),
(109, 'Lipa', '2022-09-30', 'Mains', 7569.00, 7663.00, 94.00, 3010.00, 32.02, 1.40060, 0.00140),
(110, 'Lipa', '2022-09-30', 'Drinking Water', 7603.00, 7690.00, 87.00, 2360.00, 27.13, 1.29630, 0.00130),
(111, 'Lipa', '2022-10-30', 'Mains', 7689.00, 7768.00, 79.00, 2040.00, 25.82, 1.17710, 0.00118),
(112, 'Lipa', '2022-10-31', 'Mains', 7663.00, 7752.00, 89.00, 2670.00, 30.00, 1.32610, 0.00133),
(113, 'Lipa', '2022-10-30', 'Drinking Water', 7690.00, 7781.00, 91.00, 3000.00, 32.97, 1.35590, 0.00136),
(114, 'Lipa', '2022-11-29', 'Mains', 7768.00, 7843.00, 75.00, 2330.00, 31.07, 1.11750, 0.00112),
(115, 'Lipa', '2022-11-30', 'Mains', 7752.00, 7856.00, 104.00, 3210.00, 30.87, 1.54960, 0.00155),
(116, 'Lipa', '2022-11-30', 'Drinking Water', 7781.00, 7873.00, 92.00, 2945.00, 32.01, 1.37080, 0.00137),
(117, 'Lipa', '2022-12-31', 'Mains', 7843.00, 7941.00, 98.00, 2900.00, 29.59, 1.46020, 0.00146),
(118, 'Lipa', '2022-12-31', 'Mains', 7856.00, 7925.00, 69.00, 2100.00, 30.43, 1.02810, 0.00103),
(119, 'Lipa', '2022-12-31', 'Drinking Water', 7873.00, 7945.00, 72.00, 2777.00, 38.57, 1.07280, 0.00107),
(120, 'Lipa', '2023-01-31', 'Mains', 7941.00, 8159.00, 218.00, 5004.00, 22.95, 3.24820, 0.00325),
(121, 'Lipa', '2023-01-31', 'Mains', 7925.00, 8121.00, 196.00, 3890.00, 19.85, 2.92040, 0.00292),
(122, 'Lipa', '2023-01-31', 'Drinking Water', 7945.00, 8120.00, 175.00, 2770.00, 15.83, 2.60750, 0.00261),
(123, 'Lipa', '2023-02-28', 'Mains', 8159.00, 8263.00, 104.00, 2600.00, 25.00, 1.54960, 0.00155),
(124, 'Lipa', '2023-02-27', 'Mains', 8121.00, 8234.00, 113.00, 2870.00, 25.40, 1.68370, 0.00168),
(125, 'Lipa', '2023-02-28', 'Drinking Water', 8120.00, 8225.00, 105.00, 2679.00, 25.51, 1.56450, 0.00156),
(126, 'Lipa', '2023-03-31', 'Mains', 8263.00, 8469.00, 206.00, 3900.00, 18.93, 3.06940, 0.00307),
(127, 'Lipa', '2023-03-30', 'Mains', 8234.00, 8390.00, 156.00, 3987.00, 25.56, 2.32440, 0.00232),
(128, 'Lipa', '2023-03-30', 'Drinking Water', 8225.00, 8356.00, 131.00, 3575.00, 27.29, 1.95190, 0.00195),
(129, 'Lipa', '2023-04-30', 'Mains', 8469.00, 8596.00, 127.00, 3890.00, 30.63, 1.89230, 0.00189),
(130, 'Lipa', '2023-04-29', 'Mains', 8390.00, 8563.00, 173.00, 3890.00, 22.49, 2.57770, 0.00258),
(131, 'Lipa', '2023-04-30', 'Drinking Water', 8356.00, 8563.00, 207.00, 4890.00, 23.62, 3.08430, 0.00308),
(132, 'Lipa', '2023-05-30', 'Mains', 8596.00, 8745.00, 149.00, 3480.00, 23.36, 2.22010, 0.00222),
(133, 'Lipa', '2023-05-31', 'Mains', 8563.00, 8710.00, 147.00, 3410.00, 23.20, 2.19030, 0.00219),
(134, 'Lipa', '2023-05-31', 'Drinking Water', 8563.00, 8703.00, 140.00, 3200.00, 22.86, 2.08600, 0.00209),
(135, 'Lipa', '2023-06-30', 'Mains', 8745.00, 8852.00, 107.00, 3350.00, 31.31, 1.59430, 0.00159),
(136, 'Lipa', '2023-06-30', 'Mains', 8710.00, 8908.00, 198.00, 4210.00, 21.26, 2.95020, 0.00295),
(137, 'Lipa', '2023-06-30', 'Drinking Water', 8703.00, 8863.00, 160.00, 3670.00, 22.94, 2.38400, 0.00238),
(138, 'Lipa', '2023-07-31', 'Mains', 8852.00, 8956.00, 104.00, 2335.00, 22.45, 1.54960, 0.00155),
(139, 'Lipa', '2023-07-30', 'Mains', 8908.00, 9020.00, 112.00, 4110.00, 36.70, 1.66880, 0.00167),
(140, 'Lipa', '2023-07-31', 'Drinking Water', 8863.00, 9005.00, 142.00, 4500.00, 31.69, 2.11580, 0.00212),
(141, 'Lipa', '2023-08-31', 'Mains', 8956.00, 9063.00, 107.00, 3200.00, 29.91, 1.59430, 0.00159),
(142, 'Lipa', '2023-08-31', 'Mains', 9020.00, 9173.00, 153.00, 4900.00, 32.03, 2.27970, 0.00228),
(143, 'Lipa', '2023-08-31', 'Drinking Water', 9005.00, 9123.00, 118.00, 3040.00, 25.76, 1.75820, 0.00176),
(144, 'Lipa', '2023-09-30', 'Mains', 9063.00, 9195.00, 132.00, 4090.00, 30.98, 1.96680, 0.00197),
(145, 'Lipa', '2023-09-30', 'Mains', 9173.00, 9275.00, 102.00, 4100.00, 40.20, 1.51980, 0.00152),
(146, 'Lipa', '2023-09-30', 'Drinking Water', 9123.00, 9247.00, 124.00, 3980.00, 32.10, 1.84760, 0.00185),
(147, 'Lipa', '2023-10-30', 'Mains', 9195.00, 9305.00, 110.00, 3700.00, 33.64, 1.63900, 0.00164),
(148, 'Lipa', '2023-10-30', 'Mains', 9275.00, 9394.00, 119.00, 4500.00, 37.82, 1.77310, 0.00177),
(149, 'Lipa', '2023-10-11', 'Drinking Water', 9247.00, 9360.00, 113.00, 3502.00, 30.99, 1.68370, 0.00168),
(150, 'Lipa', '2023-11-29', 'Mains', 9305.00, 9481.00, 176.00, 4990.00, 28.35, 2.62240, 0.00262),
(151, 'Lipa', '2023-11-30', 'Mains', 9394.00, 9500.00, 106.00, 3367.00, 31.76, 1.57940, 0.00158),
(152, 'Lipa', '2023-11-11', 'Drinking Water', 9360.00, 9478.00, 118.00, 4008.00, 33.97, 1.75820, 0.00176),
(153, 'Lipa', '2023-12-30', 'Mains', 9481.00, 9590.00, 109.00, 3980.00, 36.51, 1.62410, 0.00162),
(154, 'Lipa', '2023-12-31', 'Mains', 9500.00, 9592.00, 92.00, 2340.00, 25.43, 1.37080, 0.00137),
(155, 'Lipa', '2023-12-31', 'Drinking Water', 9478.00, 9596.00, 118.00, 3450.00, 29.24, 1.75820, 0.00176),
(156, 'Lipa', '2024-01-22', 'Mains', 9590.00, 9643.00, 53.00, 1575.00, 29.72, 0.78970, 0.00079),
(157, 'Lipa', '2024-01-22', 'Mains', 9592.00, 9709.00, 117.00, 2031.60, 17.36, 1.74330, 0.00174),
(158, 'Lipa', '2024-01-22', 'Drinking Water', 9596.00, 10353.00, 757.00, 70000.00, 92.47, 11.27930, 0.01128),
(159, 'Lipa', '2024-02-22', 'Mains', 9643.00, 9715.00, 72.00, 2123.10, 29.49, 1.07280, 0.00107),
(160, 'Lipa', '2024-02-22', 'Mains', 9709.00, 9791.00, 82.00, 2031.60, 24.78, 1.22180, 0.00122),
(161, 'Lipa', '2024-02-22', 'Drinking Water', 10353.00, 11110.00, 757.08, 7000.00, 9.25, 11.28052, 0.01128),
(162, 'Lipa', '2024-03-22', 'Mains', 9715.00, 9831.00, 116.00, 3390.30, 29.23, 1.72840, 0.00173),
(163, 'Lipa', '2024-03-22', 'Mains', 9791.00, 9950.00, 159.00, 4249.20, 26.72, 2.36910, 0.00237),
(164, 'Lipa', '2024-03-22', 'Drinking Water', 11110.00, 11867.00, 757.08, 7000.00, 9.25, 11.28052, 0.01128),
(165, 'Lipa', '2024-04-22', 'Mains', 9831.00, 9966.00, 135.00, 3937.50, 29.17, 2.01150, 0.00201),
(166, 'Lipa', '2024-04-22', 'Mains', 9950.00, 10182.00, 232.00, 6351.60, 27.38, 3.45680, 0.00346),
(167, 'Lipa', '2024-04-22', 'Drinking Water', 11867.00, 12624.00, 757.08, 7000.00, 9.25, 11.28052, 0.01128),
(168, 'Lipa', '2024-05-22', 'Mains', 9966.00, 10043.00, 77.00, 2267.10, 29.44, 1.14730, 0.00115),
(169, 'Lipa', '2024-05-22', 'Mains', 10182.00, 10359.00, 177.00, 4767.60, 26.94, 2.63730, 0.00264),
(170, 'Lipa', '2024-05-22', 'Drinking Water', 12624.00, 13381.00, 757.00, 7000.00, 9.25, 11.27930, 0.01128),
(171, 'Lipa', '2024-06-22', 'Mains', 10043.00, 10109.00, 66.00, 1950.30, 29.55, 0.98340, 0.00098),
(172, 'Lipa', '2024-06-22', 'Mains', 10359.00, 10440.00, 81.00, 2002.80, 24.73, 1.20690, 0.00121),
(173, 'Lipa', '2024-06-22', 'Drinking Water', 13381.00, 14138.00, 757.08, 7000.00, 9.25, 11.28052, 0.01128),
(185, 'Lobo', '2024-11-05', 'Mains', 34.00, 45.00, 32.00, 33.00, 1.03, 0.47680, 0.00048),
(186, 'Lipa', '2024-07-16', 'Deep Well', 592.00, 684.00, 350.00, 7845.00, 22.41, 5.21500, 0.00522),
(187, 'Lipa', '2024-08-16', 'Deep Well', 558.00, 754.00, 350.00, 1245.36, 3.56, 5.21500, 0.00522),
(188, 'Lipa', '2024-09-30', 'Mains', 900.00, 1200.00, 300.00, 700.00, 2.33, 4.47000, 0.00447),
(189, 'Lipa', '2024-10-30', 'Drinking Water', 800.00, 900.00, 100.00, 1000.00, 10.00, 1.49000, 0.00149),
(190, 'Lipa', '2019-01-16', 'Mains', 234.00, 265.00, 31.00, 3000.00, 96.77, 0.46190, 0.00046),
(191, 'Lipa', '2019-01-23', 'Mains', 234.00, 265.00, 31.00, 3400.00, 109.68, 0.46190, 0.00046),
(192, 'Lipa', '2019-02-13', 'Mains', 269.00, 294.00, 25.00, 2300.00, 92.00, 0.37250, 0.00037),
(193, 'Lipa', '2019-03-20', 'Mains', 345.00, 378.00, 378.00, 33.00, 0.09, 5.63220, 0.00563),
(194, 'Lipa', '2019-04-25', 'Drinking Water', 456.00, 495.00, 39.00, 4567.00, 117.10, 0.58110, 0.00058),
(195, 'Lipa', '2019-05-14', 'Drinking Water', 890.00, 923.00, 33.00, 5689.00, 172.39, 0.49170, 0.00049),
(196, 'Lipa', '2021-06-21', 'Drinking Water', 563.00, 658.00, 95.00, 4465.00, 47.00, 1.41550, 0.00142),
(197, 'Lipa', '2019-07-18', 'Drinking Water', 852.00, 902.00, 50.00, 4564.00, 91.28, 0.74500, 0.00075),
(198, 'Lipa', '2020-06-17', 'Deep Well', 569.00, 599.00, 30.00, 5900.00, 196.67, 0.44700, 0.00045),
(199, 'Lipa', '2019-08-21', 'Deep Well', 548.00, 569.00, 21.00, 3455.00, 164.52, 0.31290, 0.00031),
(200, 'Lipa', '2019-09-18', 'Deep Well', 652.00, 672.00, 20.00, 5674.00, 283.70, 0.29800, 0.00030),
(201, 'Lipa', '2020-10-20', 'Deep Well', 456.00, 489.00, 33.00, 4589.00, 139.06, 0.49170, 0.00049),
(202, 'Lipa', '2019-11-19', 'Deep Well', 993.00, 969.00, 24.00, 2189.00, 91.21, 0.35760, 0.00036),
(203, 'Lipa', '2019-12-04', 'Mains', 897.00, 937.00, 43.00, 2567.00, 59.70, 0.64070, 0.00064);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `electricity_consumption`
--
ALTER TABLE `electricity_consumption`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuel_emissions`
--
ALTER TABLE `fuel_emissions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblaccommodation`
--
ALTER TABLE `tblaccommodation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblflight`
--
ALTER TABLE `tblflight`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tblfoodwaste`
--
ALTER TABLE `tblfoodwaste`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbllpg`
--
ALTER TABLE `tbllpg`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblsignin`
--
ALTER TABLE `tblsignin`
  ADD PRIMARY KEY (`userID`);

--
-- Indexes for table `tblsolidwastesegregated`
--
ALTER TABLE `tblsolidwastesegregated`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblsolidwasteunsegregated`
--
ALTER TABLE `tblsolidwasteunsegregated`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbltreatedwater`
--
ALTER TABLE `tbltreatedwater`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tblwater`
--
ALTER TABLE `tblwater`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `electricity_consumption`
--
ALTER TABLE `electricity_consumption`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=203;

--
-- AUTO_INCREMENT for table `fuel_emissions`
--
ALTER TABLE `fuel_emissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=273;

--
-- AUTO_INCREMENT for table `tblaccommodation`
--
ALTER TABLE `tblaccommodation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=144;

--
-- AUTO_INCREMENT for table `tblflight`
--
ALTER TABLE `tblflight`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `tblfoodwaste`
--
ALTER TABLE `tblfoodwaste`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=147;

--
-- AUTO_INCREMENT for table `tbllpg`
--
ALTER TABLE `tbllpg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=193;

--
-- AUTO_INCREMENT for table `tblsolidwastesegregated`
--
ALTER TABLE `tblsolidwastesegregated`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=246;

--
-- AUTO_INCREMENT for table `tblsolidwasteunsegregated`
--
ALTER TABLE `tblsolidwasteunsegregated`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=137;

--
-- AUTO_INCREMENT for table `tbltreatedwater`
--
ALTER TABLE `tbltreatedwater`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202;

--
-- AUTO_INCREMENT for table `tblwater`
--
ALTER TABLE `tblwater`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=204;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
