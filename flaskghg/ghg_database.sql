-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 02, 2024 at 08:13 PM
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
(20, 'Balayan', 'Mains', 'February', 'Q1', '2022', 200, 400, 350, 4000, 70000, 0.05714285714285714, 49854.00000000001, 49.854000000000006),
(35, 'Central', 'Mains', 'January', 'Q1', '2023', 150, 160, 350, 500, 3500, 0.14285714285714285, 2492.7000000000003, 2.4927),
(36, 'ARASOF-Nasugbu', 'Solar', 'January', 'Q1', '2021', 150, 155, 350, 500, 1750, 0.2857142857142857, 1246.3500000000001, 1.24635),
(41, 'Central', 'Mains', 'January', 'Q1', '2021', 120, 125, 150, 100, 750, 0.13333333333333333, 534.1500000000001, 0.5341500000000001),
(43, 'Lemery', 'Solar', 'February', 'Q1', '2023', 120, 125, 150, 100, 750, 0.13333333333333333, 534.1500000000001, 0.5341500000000001),
(44, 'JPLPC-Malvar', 'Mains', 'July', 'Q3', '2024', 100, 120, 350, 100, 7000, 0.014285714285714285, 4985.400000000001, 4.9854),
(48, 'ARASOF-Nasugbu', 'Solar', 'January', 'Q1', '2021', 120, 124, 250, 100, 1000, 0.1, 712.2, 0.7122),
(49, 'ARASOF-Nasugbu', 'Solar', 'January', 'Q1', '2021', 120, 124, 250, 100, 1000, 0.1, 712.2, 0.7122),
(51, 'Central', 'Mains', 'February', 'Q1', '2021', 100, 105, 120, 100, 600, 0.16666666666666666, 427.32000000000005, 0.42732000000000003),
(54, 'JPLPC-Malvar', 'Solar', 'January', 'Q1', '2021', 95, 100, 120, 150, 600, 0.25, 427.32000000000005, 0.42732000000000003),
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
(140, 'Lipa', 'Mains', 'September', 'Q3', '2020', 1439, 1459, 350, 186166, 7000, 26.6, 4985.4, 4.99),
(141, 'Lipa', 'Mains', 'October', 'Q4', '2020', 1459, 1542, 350, 157588, 29050, 5.42, 20689.41, 20.69),
(142, 'Lipa', 'Mains', 'November', 'Q4', '2020', 1542, 1575, 350, 171069, 11550, 14.81, 8225.91, 8.23),
(143, 'Lipa', 'Mains', 'December', 'Q4', '2020', 1575, 1638, 350, 165026, 22050, 7.48, 15704.01, 15.7),
(145, 'Lipa', 'Mains', 'January', 'Q1', '2021', 1450, 1852, 350, 9254.25, 140700, 0.07, 100206.54, 100.21),
(146, 'Lipa', 'Mains', 'January', 'Q1', '2024', 1250, 1658, 350, 5214, 142800, 0.04, 101702.16, 101.7),
(147, 'Lipa', 'Mains', 'January', 'Q1', '2024', 2458, 3254, 350, 12584.25, 278600, 0.05, 198418.92, 198.42),
(148, 'Lipa', 'Mains', 'January', 'Q1', '2024', 1458, 3520, 350, 4582.25, 721700, 0.01, 513994.74, 513.99),
(149, 'Lipa', 'Mains', 'January', 'Q1', '2024', 2548, 3548, 350, 15820.25, 350000, 0.05, 249270, 249.27),
(150, 'Lipa', 'Mains', 'January', 'Q1', '2024', 2548, 6541, 350, 6985.75, 1397550, 0, 995335.11, 995.34),
(151, 'Lipa', 'Mains', 'January', 'Q1', '2024', 2548, 6541, 350, 6985.75, 1397550, 0, 995335.11, 995.34),
(152, 'Lipa', 'Mains', 'January', 'Q1', '2024', 1458, 3542, 350, 7102.25, 729400, 0.01, 519478.68, 519.48),
(153, 'Lipa', 'Mains', 'February', 'Q1', '2024', 1458, 2154, 350, 15200.25, 243600, 0.06, 173491.92, 173.49),
(154, 'Lipa', 'Mains', 'February', 'Q1', '2024', 1458, 2154, 350, 15200.25, 243600, 0.06, 173491.92, 173.49),
(155, 'Lipa', 'Mains', 'February', 'Q1', '2024', 1458, 2154, 350, 15200.25, 243600, 0.06, 173491.92, 173.49),
(156, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(157, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(158, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(159, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(160, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(161, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(163, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(164, 'Lipa', 'Mains', 'September', 'Q2', '2024', 1245, 1548, 350, 1250, 106050, 0.01, 75528.81, 75.53),
(165, 'Lipa', 'Mains', 'March', 'Q1', '2024', 7512, 9521, 350, 15254.15, 703150, 0.02, 500783.43, 500.78),
(166, 'Lipa', 'Mains', 'April', 'Q2', '2024', 2548, 5248, 350, 14521.25, 945000, 0.02, 673029, 673.03),
(167, 'Lipa', 'Mains', 'February', 'Q1', '2024', 2445, 6541, 350, 12548.21, 1433600, 0.01, 1021009.92, 1021.01),
(168, 'Lipa', 'Mains', 'January', 'Q1', '2024', 1258, 5214, 350, 14251.02, 1384600, 0.01, 986112.12, 986.11),
(169, 'Lipa', 'Solar', 'July', 'Q3', '2023', 5482, 9845, 350, 14582.49, 1527050, 0.01, 1087565.01, 1087.57),
(170, 'Lipa', 'Mains', 'February', 'Q1', '2024', 5412, 9845, 350, 14582.12, 1551550, 0.01, 1105013.91, 1105.01),
(171, 'Lipa', 'Mains', 'February', 'Q1', '2024', 5412, 9845, 350, 14582.12, 1551550, 0.01, 1105013.91, 1105.01),
(172, 'Lipa', 'Mains', 'January', 'Q2', '2023', 2485, 6548, 350, 14582.12, 1422050, 0.01, 1012784.01, 1012.78),
(173, 'Lipa', 'Mains', 'March', 'Q2', '2023', 1485, 5248, 350, 25482.12, 1317050, 0.02, 938003.01, 938),
(174, 'Alangilan', 'Solar', 'January', 'Q1', '2021', 1452, 3354, 350, 1254.12, 665700, 0, 474111.54, 474.11),
(176, 'Lipa', 'Mains', 'October', 'Q4', '2024', 10258, 15254, 350, 251254, 1748600, 0.14, 1245352.92, 1245.35);

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
  `quantity_liters` decimal(5,2) DEFAULT NULL,
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
(124, 'Lipa', '2024-03-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1750, 205.00, 11955.1, 525.13, 0.564987, 9.24484, 534.94, 0.53494),
(125, 'Lipa', '2024-04-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1732, 191.00, 11537.6, 488.733, 0.525828, 8.60407, 497.863, 0.497863),
(126, 'Lipa', '2024-05-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1982, 148.00, 8611.13, 380.665, 0.409557, 6.70155, 387.776, 0.387776),
(127, 'Lipa', '2024-06-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1705, 182.00, 10513.9, 465.908, 0.50127, 8.20224, 474.611, 0.474611),
(129, 'Lipa', '2023-01-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 849, 91.00, 5872, 234.513, 0.252313, 4.12857, 238.894, 0.238894),
(134, 'Lipa', '2023-02-28', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 926, 53.00, 3204.6, 136.516, 0.146877, 2.40334, 139.066, 0.139066),
(135, 'Lipa', '2023-03-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1149, 149.00, 8579.56, 382.378, 0.4114, 6.7317, 389.521, 0.389521),
(136, 'Lipa', '2023-04-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1137, 134.00, 7658.77, 344.523, 0.370672, 6.06528, 350.959, 0.350959),
(137, 'Lipa', '2023-05-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 2008, 124.00, 6685.84, 318.35, 0.342512, 5.6045, 324.297, 0.324297),
(140, 'Lipa', '2023-06-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1204, 143.00, 7710.41, 367.272, 0.395148, 6.46576, 374.133, 0.374133),
(141, 'Lipa', '2023-07-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 2187, 186.00, 10311.5, 475.569, 0.511665, 8.37233, 484.453, 0.484453),
(142, 'Lipa', '2023-08-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1606, 193.00, 11996.3, 495.787, 0.533418, 8.72826, 505.049, 0.505049),
(143, 'Lipa', '2023-09-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 2628, 230.00, 15381.7, 588.647, 0.633325, 10.363, 599.643, 0.599643),
(145, 'Lipa', '2023-10-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 2446, 200.00, 12911.3, 511.967, 0.550825, 9.0131, 521.531, 0.521531),
(146, 'Lipa', '2023-11-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 2904, 208.00, 12539.1, 532.568, 0.57299, 9.37578, 542.517, 0.542517),
(147, 'Lipa', '2023-12-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1333, 224.00, 12274.7, 573.106, 0.616605, 10.0895, 583.812, 0.583812),
(148, 'Lipa', '2022-01-31', 'Ana M.', 'Vehicle', 'Nissan Urvan', 'KOC825', 'fuel', 'Diesel', 'Diesel Max', '1356', 1682, 122.00, 6803.09, 313.084, 0.336848, 5.51181, 318.933, 0.318933),
(149, 'Lipa', '2022-02-28', 'Ana M.', 'Vehicle', 'Mitsubishi L300 FB Van', 'SKT627', 'fuel', 'Diesel', 'Diesel Max', '1107', 1305, 163.00, 8250.21, 417.906, 0.449625, 7.35717, 425.713, 0.425713),
(150, 'Lipa', '2022-03-31', 'John D.', 'Vehicle', 'Isuzu Sportivo', 'A6F875', 'fuel', 'Diesel', 'Diesel Max', '1581', 1136, 124.00, 7769.88, 317.097, 0.341165, 5.58245, 323.021, 0.323021),
(151, 'Lipa', '2022-04-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '1596', 1730, 112.00, 7761.3, 287.422, 0.309238, 5.06003, 292.791, 0.292791),
(152, 'Lipa', '2022-05-31', 'Ana M.', 'Vehicle', 'Honda Civic', 'P9T902', 'fuel', 'Diesel', 'Diesel Max', '1800', 1407, 123.00, 6563.65, 314.465, 0.338333, 5.5361, 320.339, 0.320339),
(153, 'Lipa', '2022-06-30', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '1298', 1597, 63.00, 3634.96, 162.971, 0.17534, 2.86907, 166.015, 0.166015),
(154, 'Lipa', '2022-07-31', 'Maria S.', 'Vehicle', 'Toyota Avanza', 'B8B575', 'fuel', 'Diesel', 'Diesel Max', '1137', 1307, 81.00, 5157.05, 208.237, 0.224043, 3.66599, 212.127, 0.212127),
(155, 'Lipa', '2022-08-31', 'John D.', 'Vehicle', 'Hyundai Starex', 'P9M902', 'fuel', 'Diesel', 'Diesel Max', '1506', 1158, 56.00, 3948.23, 145.309, 0.156337, 2.55814, 148.023, 0.148023),
(156, 'Lipa', '2022-09-30', 'Maria S.', 'Vehicle', 'Toyota Hilux', 'SKT626', 'fuel', 'Diesel', 'Diesel Max', '1092', 1931, 78.00, 5946.45, 201.592, 0.216892, 3.54899, 205.358, 0.205358),
(157, 'Lipa', '2022-10-31', 'Ana M.', 'Vehicle', 'Foton Bus', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '1926', 1347, 131.00, 6893.49, 334.913, 0.360332, 5.89609, 341.169, 0.341169),
(158, 'Lipa', '2022-11-30', 'Ana M.', 'Vehicle', 'Mitsubishi Adventure', 'S5W578', 'fuel', 'Diesel', 'Diesel Max', '1959', 1013, 131.00, 8008.9, 335.092, 0.360525, 5.89924, 341.351, 0.341351),
(159, 'Lipa', '2023-12-31', 'Roman L.', 'Vehicle', 'Nissan Urvan', 'KOC825', 'fuel', 'Diesel', 'Diesel Max', '1590', 1755, 142.00, 9583.54, 365.278, 0.393003, 6.43066, 372.102, 0.372102),
(160, 'Lipa', '2021-01-31', 'Ana M.', 'Vehicle', 'Toyota Hi-Ace', 'BOU837', 'fuel', 'Diesel', 'Diesel Max', '1190', 1298, 137.00, 7227.27, 350.862, 0.377492, 6.17688, 357.416, 0.357416),
(161, 'Lipa', '2021-02-28', 'John D.', 'Vehicle', 'Mitsubishi Adventure', 'S5W578', 'fuel', 'Diesel', 'Diesel Max', '1096', 1375, 150.00, 9655.08, 385.419, 0.414672, 6.78525, 392.619, 0.392619),
(162, 'Lipa', '2021-03-31', 'Ana M.', 'Vehicle', 'Toyota Minibus', 'S5W613', 'fuel', 'Diesel', 'Diesel Max', '1037', 1380, 147.00, 9755.09, 376.192, 0.404745, 6.62281, 383.22, 0.38322),
(163, 'Lipa', '2021-04-30', 'Ana M.', 'Vehicle', 'Mitsubishi Adventure', 'S5W578', 'fuel', 'Diesel', 'Diesel Max', '1326', 1007, 186.00, 9639.4, 477.486, 0.513727, 8.40608, 486.406, 0.486406),
(164, 'Lipa', '2021-05-31', 'Ana M.', 'Vehicle', 'Mitsubishi L300 FB Van', 'SKT627', 'fuel', 'Diesel', 'Diesel Max', '1499', 1369, 99.00, 6889.88, 255.114, 0.274478, 4.49125, 259.88, 0.25988),
(165, 'Lipa', '2021-06-30', 'Ana M.', 'Vehicle', 'Toyota Hilux', 'SKT626', 'fuel', 'Diesel', 'Diesel Max', '1926', 1067, 138.00, 8656.56, 353.623, 0.380462, 6.22547, 360.229, 0.360229),
(166, 'Lipa', '2021-07-31', 'John D.', 'Vehicle', 'Toyota Hi-Ace', 'BOU837', 'fuel', 'Diesel', 'Diesel Max', '1566', 1407, 171.00, 9909.42, 439.121, 0.47245, 7.73066, 447.324, 0.447324),
(167, 'Lipa', '2021-08-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '1010', 1801, 167.00, 9483.52, 427.21, 0.459635, 7.52097, 435.19, 0.43519),
(168, 'Lipa', '2021-09-30', 'Ana M.', 'Vehicle', 'Toyota Avanza', 'B8B575', 'fuel', 'Diesel', 'Diesel Max', '1301', 1802, 80.00, 4293.07, 204.531, 0.220055, 3.60074, 208.352, 0.208352),
(169, 'Lipa', '2021-10-31', 'Roman L.', 'Vehicle', 'Mitsubishi L300 FB Van', 'SKT627', 'fuel', 'Diesel', 'Diesel Max', '1518', 1925, 154.00, 9893.35, 393.701, 0.423582, 6.93104, 401.055, 0.401055),
(170, 'Lipa', '2021-11-30', 'Roman L.', 'Vehicle', 'Toyota Minibus', 'SEU721', 'fuel', 'Diesel', 'Diesel Max', '1200', 1173, 90.00, 4964.83, 231.318, 0.248875, 4.07232, 235.639, 0.235639),
(171, 'Lipa', '2021-12-31', 'Roman L.', 'Vehicle', 'Toyota Hi-Ace', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '1152', 1910, 121.00, 6907.21, 310.989, 0.334592, 5.47491, 316.798, 0.316798),
(172, 'Lipa', '2020-01-31', 'Ana M.', 'Vehicle', 'Honda Civic', 'P9T902', 'fuel', 'Diesel', 'Diesel Max', '1341', 1481, 97.00, 5947.39, 250.437, 0.269445, 4.4089, 255.115, 0.255115),
(173, 'Lipa', '2020-02-29', 'John D.', 'Vehicle', 'Toyota Avanza', 'B8B575', 'fuel', 'Diesel', 'Diesel Max', '1619', 1479, 108.00, 5959.93, 277.428, 0.298485, 4.88408, 282.611, 0.282611),
(174, 'Lipa', '2020-03-31', 'Ana M.', 'Vehicle', 'Isuzu Sportivo', 'A6F875', 'fuel', 'Diesel', 'Diesel Max', '1476', 1625, 100.00, 5140.29, 257.637, 0.277192, 4.53566, 262.45, 0.26245),
(175, 'Lipa', '2020-04-30', 'John D.', 'Vehicle', 'Toyota Minibus', 'S6C486', 'fuel', 'Diesel', 'Diesel Max', '1655', 1454, 124.00, 7521.73, 317.148, 0.34122, 5.58335, 323.073, 0.323073),
(176, 'Lipa', '2020-05-31', 'Ana M.', 'Vehicle', 'Toyota Avanza', 'B8B575', 'fuel', 'Diesel', 'Diesel Max', '1956', 1292, 106.00, 6617.28, 272.495, 0.293177, 4.79724, 277.586, 0.277586),
(177, 'Lipa', '2020-06-30', 'Ana M.', 'Vehicle', 'Toyota Grandia', 'SJD280', 'fuel', 'Diesel', 'Diesel Max', '1040', 1605, 150.00, 9087.43, 384.116, 0.41327, 6.7623, 391.291, 0.391291),
(178, 'Lipa', '2020-07-31', 'John D.', 'Vehicle', 'Isuzu Sportivo', 'A6F875', 'fuel', 'Diesel', 'Diesel Max', '1295', 1050, 126.00, 7202.07, 323.922, 0.348507, 5.7026, 329.973, 0.329973),
(179, 'Lipa', '2020-08-31', 'John D.', 'Vehicle', 'Isuzu Traviz', 'SHS165', 'fuel', 'Diesel', 'Diesel Max', '1352', 1776, 107.00, 5512.75, 274.617, 0.29546, 4.83459, 279.747, 0.279747),
(180, 'Lipa', '2020-09-30', 'John D.', 'Vehicle', 'Nissan Urvan', 'KOC825', 'fuel', 'Diesel', 'Diesel Max', '1668', 1811, 68.00, 4538.74, 174.268, 0.187495, 3.06796, 177.524, 0.177524),
(181, 'Lipa', '2020-11-30', 'Ana M.', 'Vehicle', 'Toyota Avanza', 'B8B575', 'fuel', 'Diesel', 'Diesel Max', '1560', 1909, 137.00, 7794.8, 350.581, 0.37719, 6.17193, 357.13, 0.35713),
(182, 'Lipa', '2020-12-31', 'Roman L.', 'Vehicle', 'Mitsubishi Adventure', 'S5W578', 'fuel', 'Diesel', 'Diesel Max', '1389', 1048, 53.00, 3563.13, 137.615, 0.14806, 2.42269, 140.186, 0.140186),
(183, 'Lipa', '2024-11-30', 'Roman L.', 'Vehicle', 'Toyota Hilux', 'S5S618', 'fuel', 'Diesel', 'Diesel Max', '0000', 1245, 25.00, 1000.25, 65.2291, 0.07018, 1.14835, 66.4476, 0.0664476);

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
(9, 'Lipa', 'OVCDEA', '2022', 'Dianne', 'Conference', '2024-10-04', '2024-10-12', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(10, 'Lipa', 'OVCDEA', '2022', 'Dianne', 'Conference', '2024-10-04', '2024-10-12', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(11, 'Lipa', 'OVCDEA', '2022', 'Dianne', 'Conference', '2024-10-04', '2024-10-12', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(12, 'Central', 'OVCDEA', '2023', 'Kyla', 'Meeting', '2024-09-13', '2024-09-15', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(13, 'Central', 'OVCDEA', '2023', 'Kyla', 'Meeting', '2024-09-13', '2024-09-15', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(14, 'Central', 'OVCDEA', '2023', 'Kyla', 'Meeting', '2024-09-13', '2024-09-15', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(15, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(16, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(17, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(18, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(19, 'Central', 'OVCDEA', '2024', 'Keon', 'Awarding', '2024-09-15', '2024-09-18', 'Philippines', 'Local', 2, 3, 66.54, 399.24, 0.40),
(20, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(21, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(22, 'ARASOF-Nasugbu', 'OVCDEA', '2022', 'Lester', 'Awarding', '2024-09-15', '2024-09-17', 'Philippines', 'Local', 1, 1, 66.54, 66.54, 0.07),
(23, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(24, 'ARASOF-Nasugbu', 'OVCDEA', '2022', 'Dianne', 'Meeting', '2024-09-15', '2024-09-18', 'Philippines', 'Local', 1, 2, 66.54, 133.08, 0.13),
(25, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(26, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(27, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(28, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(29, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(30, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(31, 'Balayan', 'OVCDEA', '2022', 'Kyla', 'Conference', '2024-09-15', '2024-09-17', 'Philippines', 'International', 2, 2, 66.54, 266.16, 0.27),
(32, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(33, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(34, 'Lemery', 'OVCDEA', '2024', 'Kyla', 'Seminar', '2024-09-17', '2024-09-20', 'Philippines', 'Local', 3, 2, 66.54, 399.24, 0.40),
(35, 'San Juan', 'RGO', '2023', 'Dianne', 'Conference', '2024-10-12', '2024-10-15', 'Bosnia and Herzegovina', 'International', 3, 3, 16.04, 144.36, 0.14),
(36, 'ARASOF-Nasugbu', 'RGO', '2022', 'Dianne', 'Conference', '2024-09-15', '2024-09-17', '', 'Local', 1, 1, 0.00, 0.00, 0.00),
(37, 'ARASOF-Nasugbu', 'OVCDEA', '2023', 'Dianne Kristel', 'Conference', '2024-09-18', '2024-09-20', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(38, 'Central', 'OVCDEA', '2022', 'Dianne Kristel', 'Conference', '2024-09-21', '2024-09-23', 'Zimbabwe', 'Local', 1, 4, 60.12, 240.48, 0.24),
(39, 'Central', 'OVCDEA', '2022', 'Lester', 'Seminar', '2024-09-01', '2024-09-05', 'Philippines', 'Local', 1, 1, 66.54, 66.54, 0.07),
(40, 'Alangilan', 'OVCDEA', '2024', 'Dianne Kristel', 'Meeting', '2024-09-22', '2024-10-02', 'Philippines', 'International', 10, 10, 66.54, 6654.00, 6.65),
(41, 'Central', 'OVCDEA', '2023', 'Dianne', 'Meeting', '2024-09-25', '2024-09-30', 'Philippines', 'International', 2, 2, 66.54, 266.16, 0.27),
(42, 'Central', 'OVCDEA', '2022', 'Dianne Kristel', 'Awarding', '2024-09-27', '2024-09-30', 'Argentina', 'International', 5, 5, 77.08, 1927.00, 1.93),
(43, 'Central', 'OVCDEA', '2024', 'Lester Rhoy', 'Seminar', '2024-10-01', '2024-10-05', 'Philippines', 'Local', 4, 4, 66.54, 1064.64, 1.06),
(44, 'Central', 'RGO', '2023', 'Kyla Claire', 'Conference', '2024-09-28', '2024-10-01', 'Belarus', 'International', 3, 3, 18.73, 168.57, 0.17),
(45, 'Central', 'RGO', '2022', 'Dianne', 'Conference', '2024-09-27', '2024-09-30', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(46, 'Central', 'OVCDEA', '2024', 'Verlon', 'Conference', '2024-09-28', '2024-09-30', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(47, 'Balayan', 'OVCDEA', '2023', 'Keon', 'Awarding', '2024-09-27', '2024-10-03', 'Australia', 'International', 5, 5, 51.47, 1286.75, 1.29),
(48, 'ARASOF-Nasugbu', 'OVCDEA', '2022', 'Dianne', 'Conference', '2024-09-27', '2024-10-01', 'Bosnia and Herzegovina', 'Local', 8, 8, 16.04, 1026.56, 1.03),
(49, 'Central', 'OVCDEA', '2023', 'Kyla', 'Awarding', '2024-09-27', '2024-09-28', 'Philippines', 'Local', 1, 1, 66.54, 66.54, 0.07),
(50, 'Central', 'OVCDEA', '2022', 'Dianne', 'Meeting', '2024-09-27', '2024-09-29', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(51, 'ARASOF-Nasugbu', 'OVCDEA', '2022', 'Lester', 'Conference', '2024-09-26', '2024-09-30', 'Armenia', 'International', 5, 5, 77.08, 1927.00, 1.93),
(52, 'Balayan', 'RGO', '2022', 'Dianne', 'Conference', '2024-09-27', '2024-09-30', 'Belize', 'International', 5, 5, 16.04, 401.00, 0.40),
(53, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(54, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(55, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(56, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(57, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(58, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(59, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(60, 'Central', 'OVCDEA', '2023', 'Dianne Kristel', 'Meeting', '2024-09-27', '2024-10-01', 'Brazil', 'International', 4, 4, 16.77, 268.32, 0.27),
(61, 'Central', 'RGO', '2023', 'Dianne Kristel', 'Awarding', '2024-09-28', '2024-09-30', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(62, 'JPLPC-Malvar', 'RGO', '2023', 'Lester Rhoy', 'Conference', '2024-09-28', '2024-10-01', 'Botswana', 'International', 4, 4, 16.04, 256.64, 0.26),
(63, 'Balayan', 'OVCDEA', '2023', 'Dianne Kristel', 'Conference', '2024-09-28', '2024-09-30', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(64, 'Lipa', 'OVCDEA', '2022', 'Kyla', 'Conference', '2024-10-01', '2024-10-04', 'Philippines', 'Local', 3, 3, 66.54, 598.86, 0.60),
(65, 'Lipa', 'RGO', '2022', 'Dianne', 'Awarding', '2024-10-01', '2024-10-05', 'Australia', 'International', 4, 4, 51.47, 823.52, 0.82),
(66, 'Lipa', 'OVCDEA', '2022', 'Dianne', 'Conference', '2024-10-11', '2024-10-17', 'France', 'International', 7, 7, 8.01, 392.49, 0.39),
(69, 'Lipa', NULL, '2024', 'Keon', 'Conference', '2024-10-25', '2024-10-30', 'Benin', 'Local', 5, 5, 16.04, 401.00, 0.40),
(70, 'Lipa', 'RGO', '2022', 'Dianne', 'Conference', '2024-10-16', '2024-10-20', 'Brazil', 'Local', 8, 8, 16.77, 1073.28, 1.07),
(71, 'Lipa', 'OVCDEA', '2021', 'Lester Rhoy', 'Seminar', '2024-10-31', '2024-11-02', 'Argentina', 'International', 3, 3, 77.08, 693.72, 0.69),
(72, 'Lipa', 'OVCDEA', '2020', 'Richelle', 'Conference', '2024-10-24', '2024-10-26', 'Philippines', 'Local', 2, 2, 66.54, 266.16, 0.27),
(73, 'Lipa', 'OVCDEA', '2020', 'Kyla', 'Conference', '2024-10-15', '2024-10-20', 'Philippines', 'Local', 1, 5, 66.54, 332.70, 0.33),
(74, 'Lipa', 'RGO', '2021', 'Dianne Kristel', 'Conference', '2024-10-15', '2024-10-22', 'Philippines', 'Local', 1, 7, 66.54, 465.78, 0.47);

-- --------------------------------------------------------

--
-- Table structure for table `tblcampus`
--

CREATE TABLE `tblcampus` (
  `ID` int(11) NOT NULL,
  `Campus` char(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblelectricity`
--

CREATE TABLE `tblelectricity` (
  `Campus` char(20) DEFAULT NULL,
  `Category` char(20) DEFAULT NULL,
  `Month` varchar(20) DEFAULT NULL,
  `Quarter` varchar(10) DEFAULT NULL,
  `YearTransact` year(4) DEFAULT NULL,
  `PreviousReading` varchar(30) DEFAULT NULL,
  `CurrentReading` varchar(30) DEFAULT NULL,
  `Multiplier` varchar(20) DEFAULT NULL,
  `TotalAmount` varchar(20) DEFAULT NULL,
  `Consumption` varchar(20) DEFAULT NULL,
  `PricePerKWH` varchar(20) DEFAULT NULL,
  `FactorKGCO2/kWh` varchar(20) DEFAULT NULL,
  `FactorTCO2/kWh` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `GHGEmissionKGC02e` double DEFAULT NULL,
  `GHGEmissionTC02e` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tblflight`
--

INSERT INTO `tblflight` (`ID`, `Campus`, `Office`, `Year`, `TravellerName`, `TravelPurpose`, `TravelDate`, `DomesticInternational`, `Origin`, `Destination`, `Class`, `OnewayRoundTrip`, `GHGEmissionKGC02e`, `GHGEmissionTC02e`) VALUES
(8, 'Lipa', 'OVCDEA', '2024', 'Dianne', 'Meeting', '2024-10-30', 'Domestic', 'MNL', 'DVA', 'Business Class', 'One Way', 25.25, 0.25);

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
(1, 'Lipa', '2022', 'October', 'Auxillary Services', 'Meal,Vegetarian', 5, 14.25, 0.01425),
(2, 'Lipa', '2022', 'September', 'Auxillary Services', 'Meal,Vegetarian', 5, 14.25, 0.01425),
(13, 'Lipa', '2024', 'January', 'Procurement', '1 Average Meal', 10, 47, 0.047),
(18, 'Balayan', '2021', 'September', 'Auxillary Services', '1 Average Meal', 20, 94, 0.094),
(19, 'Alangilan', '2022', 'October', 'Auxillary Services', 'Meal,Vegan', 120, 202.79999999999998, 0.20279999999999998),
(20, 'ARASOF-Nasugbu', '2021', 'November', 'Auxillary Services', '1 Average Meal', 205, 963.5, 0.9635),
(21, 'ARASOF-Nasugbu', '2021', 'October', 'Procurement', 'Meal,Vegetarian', 25, 71.25, 0.07125),
(22, 'Lemery', '2022', 'February', 'Procurement', '1 Average Meal', 5, 23.5, 0.0235),
(23, 'Lipa', '2021', 'January', 'Procurement', '1 Cold or Hot Snack', 2, 4.04, 0.00404),
(24, 'JPLPC-Malvar', '2022', 'January', 'Auxillary Services', 'Meal with Beef', 10, 69.3, 0.0693),
(25, 'Lipa', '2021', 'January', 'Procurement', 'Meal with Beef', 20, 138.6, 0.1386),
(26, 'Lipa', '2024', 'January', 'Auxillary Services', '1 Sandwich', 30, 38.1, 0.0381),
(27, 'Lipa', '2022', 'April', 'Auxillary Services', 'Meal with Beef', 10, 69.3, 0.0693),
(28, 'Lipa', '2024', 'April', 'Auxillary Services', '1 Average Meal', 18, 84.60000000000001, 0.08460000000000001),
(29, 'Lipa', '2021', 'January', 'Procurement', '1 Sandwich', 11, 13.97, 0.01397),
(30, 'Lipa', '2022', 'April', 'RGO', 'Meal with Chicken', 2, 6.78, 0.0067800000000000004),
(31, 'Lipa', '2021', 'January', 'Procurement', 'Meal with Beef', 3, 20.79, 0.02079),
(32, 'Lipa', '2023', 'October', 'Auxillary Services', '1 Hot Snack (burger and fries)', 11, 30.47, 0.03047),
(33, 'Lipa', '2022', 'January', 'Procurement', '1 Standard Breakfast', 7, 5.88, 0.00588),
(34, 'Lipa', '2023', 'May', 'Procurement', 'Meal with Chicken', 12, 40.68, 0.04068),
(35, 'Lipa', '2021', 'January', 'Procurement', 'Meal,Vegan', 4, 6.76, 0.0067599999999999995),
(36, 'Lipa', '2021', 'January', 'Procurement', 'Meal,Vegan', 4, 6.76, 0.0067599999999999995),
(37, 'Lipa', '2022', 'February', 'Auxillary Services', 'Meal with Beef', 15, 103.94999999999999, 0.10394999999999999),
(38, 'Lipa', '2022', 'February', 'Auxillary Services', 'Meal with Beef', 15, 103.94999999999999, 0.10394999999999999),
(39, 'Lipa', '2022', 'February', 'Auxillary Services', 'Meal with Beef', 15, 103.94999999999999, 0.10394999999999999),
(40, 'Lipa', '2022', 'February', 'Auxillary Services', 'Meal with Beef', 15, 103.94999999999999, 0.10394999999999999),
(41, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Standard Breakfast', 17, 14.28, 0.01428),
(42, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Standard Breakfast', 17, 14.28, 0.01428),
(43, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Standard Breakfast', 17, 14.28, 0.01428),
(44, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Standard Breakfast', 17, 14.28, 0.01428),
(45, 'Lipa', '2023', 'March', 'Auxillary Services', '1 Standard Breakfast', 17, 14.28, 0.01428),
(46, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(47, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(48, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(49, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(50, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(51, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(52, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(53, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(54, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(55, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(56, 'Lipa', '2023', 'April', 'Auxillary Services', '1 Sandwich', 12, 15.24, 0.01524),
(57, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(58, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(59, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(60, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(61, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(62, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(63, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(64, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(65, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(66, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(67, 'Lipa', '2023', 'February', 'Procurement', 'Meal,Vegetarian', 8, 22.8, 0.0228),
(68, 'Lipa', '2021', 'March', 'Procurement', 'Meal with Beef', 15, 103.94999999999999, 0.10394999999999999),
(69, 'Lipa', '2023', 'August', 'Auxillary Services', 'Meal with Chicken', 15, 50.85, 0.05085),
(70, 'Lipa', '2022', 'January', 'Procurement', '1 Gourmet Breakfast', 12, 27.96, 0.027960000000000002),
(71, 'Lipa', '2021', 'March', 'Auxillary Services', 'Meal with Beef', 18, 124.74, 0.12473999999999999),
(72, 'Lipa', '2021', 'November', 'RGO', '1 Average Meal', 4, 18.8, 0.0188),
(74, 'Lipa', '2022', 'January', 'Procurement', '1 Sandwich', 5, 6.35, 0.00635),
(75, 'Lipa', '2022', 'June', 'Procurement', 'Meal with Beef', 7, 48.51, 0.04851),
(76, 'Lipa', '2021', 'July', 'Auxillary Services', '1 Gourmet Breakfast', 20, 46.6, 0.0466),
(77, 'Lipa', '2024', 'December', 'Auxiliary Services', 'Meal with Chicken', 25, 84.75, 0.08475);

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
  `TankWeight` varchar(20) DEFAULT NULL,
  `TankVolume` varchar(20) DEFAULT NULL,
  `TotalTankVolume` varchar(20) DEFAULT NULL,
  `GHGEmissionKGCO2e` varchar(20) DEFAULT NULL,
  `GHGEmissionTCO2e` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbllpg`
--

INSERT INTO `tbllpg` (`id`, `Campus`, `Office`, `YearTransact`, `Month`, `ConcessionariesType`, `TankQuantity`, `TankWeight`, `TankVolume`, `TotalTankVolume`, `GHGEmissionKGCO2e`, `GHGEmissionTCO2e`) VALUES
(7, 'ARASOF-Nasugbu', 'Procurement', '2022', 'May', 'Diesel', 20, '15', '29.4', '588', '1739.2746', '1.7392746'),
(8, 'ARASOF-Nasugbu', 'Procurement', '2022', 'May', 'Diesel', 20, '15', '29.4', '588', '1739.2746', '1.7392746'),
(9, 'Lipa', 'Auxiliary Services', '2023', 'August', 'Fuel', 10, '15', '29.4', '294', '869.6373', '0.8696373'),
(10, 'Lipa', 'Auxiliary Services', '2024', 'January', 'Fuel', 10, '25', '49', '490', '1449.3954999999999', '1.4493954999999998'),
(11, 'Lipa', 'Auxiliary Services', '2024', 'January', 'Fuel', 10, '25', '49', '490', '1449.3954999999999', '1.4493954999999998'),
(12, 'Lobo', 'Procurement', '2022', 'January', 'Fuel', 20, '25', '49', '980', '2898.7909999999997', '2.8987909999999997'),
(13, 'Lobo', 'Procurement', '2022', 'January', 'Fuel', 20, '25', '49', '980', '2898.7909999999997', '2.8987909999999997'),
(14, 'ARASOF-Nasugbu', 'Procurement', '2022', 'February', 'Diesel', 10, '18', '35.28', '352.8', '1043.56476', '1.04356476'),
(15, 'ARASOF-Nasugbu', 'Procurement', '2022', 'October', 'Diesel', 10, '18', '35.28', '352.8', '1043.56476', '1.04356476'),
(16, 'Balayan', 'Procurement', '2022', 'September', 'Diesel', 10, '18', '35.28', '352.8', '0', '0'),
(17, 'Balayan', 'Procurement', '2022', 'November', 'Diesel', 10, '18', '35.28', '352.8', '0', '0'),
(18, 'Balayan', 'Auxiliary Services', '2022', 'September', 'Diesel', 10, '18', '35.28', '352.8', '0', '0'),
(19, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'April', 'Diesel', 10, '18', '35.28', '352.8', '0', '0'),
(20, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'October', 'Diesel', 10, '18', '35.28', '352.8', '29.5795', '0.029579499999999998'),
(21, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'October', 'Diesel', 10, '18', '35.28', '352.8', '29.5795', '0.029579499999999998'),
(22, 'ARASOF-Nasugbu', 'Procurement', '2023', 'November', 'Diesel', 10, '18', '35.28', '352.8', '29.5795', '0.029579499999999998'),
(23, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'March', 'Diesel', 10, '18', '35.28', '352.8', '1043.56476', '1.04356476'),
(24, 'Alangilan', 'Procurement', '2022', 'October', 'Diesel', 10, '18', '35.28', '352.8', '1043.56476', '1.04356476'),
(25, 'Balayan', 'Procurement', '2022', 'June', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(26, '', '', '0000', '', '', 0, '0', '0', '0', '0', '0'),
(27, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(28, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(29, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(30, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(31, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(32, 'Balayan', 'Procurement', '2023', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(33, 'Central', 'Auxiliary Services', '2022', 'November', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(34, 'Central', 'Auxiliary Services', '2022', 'November', 'Fuel', 12, '50', '98', '1176', '177.43488', '0.17743488'),
(35, 'Central', 'Auxiliary Services', '2022', 'November', 'Fuel', 5, '200', '392', '1960', '295.72479999999996', '0.29572479999999995'),
(36, 'Central', 'Auxiliary Services', '2022', 'November', 'Diesel', 5, '200', '392', '1960', '295.72479999999996', '0.29572479999999995'),
(37, 'Central', 'Procurement', '2023', 'August', 'Fuel', 12, '50', '98', '1176', '177.43488', '0.17743488'),
(38, 'Central', 'Procurement', '2023', 'August', 'Diesel', 5, '200', '392', '1960', '295.72479999999996', '0.29572479999999995'),
(39, 'Central', 'Procurement', '2023', 'August', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(40, 'Central', 'Procurement', '2023', 'August', 'Fuel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(41, 'Central', 'Procurement', '2023', 'August', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(42, 'Central', 'Procurement', '2023', 'August', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(43, 'Central', 'Procurement', '2023', 'August', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(44, 'Central', 'Procurement', '2023', 'August', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(45, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'December', 'Fuel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(46, 'ARASOF-Nasugbu', 'Auxiliary Services', '2022', 'April', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(47, 'ARASOF-Nasugbu', 'Procurement', '2022', 'November', 'Diesel', 1, '1', '1.96', '1.96', '0.29572479999999995', '0.0002957248'),
(48, 'ARASOF-Nasugbu', 'Procurement', '2022', 'November', 'Diesel', 10, '18', '35.28', '352.8', '53.230464', '0.053230464'),
(49, 'ARASOF-Nasugbu', 'Procurement', '2023', 'August', 'Fuel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(50, 'ARASOF-Nasugbu', 'Procurement', '2023', 'August', 'Fuel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(51, 'ARASOF-Nasugbu', 'Procurement', '2023', 'August', 'Fuel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(52, 'ARASOF-Nasugbu', 'Procurement', '2023', 'August', 'Fuel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(53, 'ARASOF-Nasugbu', 'Auxiliary Services', '2022', 'February', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(54, 'ARASOF-Nasugbu', 'Auxiliary Services', '2022', 'February', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(55, 'JPLPC-Malvar', 'Auxiliary Services', '2022', 'November', 'Fuel', 12, '50', '98', '1176', '35.4954', '0.035495399999999996'),
(56, 'JPLPC-Malvar', 'Auxiliary Services', '2022', 'November', 'Fuel', 12, '50', '98', '1176', '35.4954', '0.035495399999999996'),
(57, 'Alangilan', 'Procurement', '2022', 'September', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(58, 'Alangilan', 'Procurement', '2022', 'September', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(59, 'Alangilan', 'Procurement', '2022', 'September', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(60, 'Alangilan', 'Procurement', '2022', 'September', 'Diesel', 1, '1', '1.96', '1.96', '2.95795', '0.00295795'),
(61, 'ARASOF-Nasugbu', 'Auxiliary Services', '2023', 'July', 'Diesel', 1, '1', '1.96', '1.96', '5.797581999999999', '0.005797581999999999'),
(62, 'Balayan', 'Procurement', '2022', 'August', 'Fuel', 1, '1', '1.96', '1.96', '5.797581999999999', '0.005797581999999999'),
(63, 'Balayan', 'Auxiliary Services', '2022', 'November', 'Diesel', 12, '50', '98', '1176', '35.4954', '0.035495399999999996'),
(64, 'Balayan', 'Auxiliary Services', '2022', 'November', 'Diesel', 12, '50', '98', '1176', '35.4954', '0.035495399999999996'),
(65, 'Central', 'Auxiliary Services', '2023', 'October', 'Fuel', 12, '50', '98', '1176', '35.4954', '0.035495399999999996'),
(66, 'Central', 'Auxiliary Services', '2023', 'October', 'Fuel', 12, '50', '98', '1176', '147.8976', '0.14789760000000002'),
(67, 'Alangilan', 'RGO', '2023', 'September', 'Fuel', 12, '50', '98', '1176', '147.8976', '0.14789760000000002'),
(68, 'Central', 'Auxiliary Services', '2023', 'April', 'Diesel', 10, '18', '35.28', '352.8', '123.24799999999999', '0.123248'),
(69, 'Lipa', 'Auxiliary Services', '2023', 'March', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(70, 'Lipa', 'Auxiliary Services', '2023', 'March', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(71, 'Lipa', 'Procurement', '2023', 'August', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(72, 'Lipa', 'Procurement', '2023', 'August', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(73, 'Lipa', 'Auxiliary Services', '2023', 'May', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(74, 'Lipa', 'Auxiliary Services', '2023', 'May', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(75, 'Lipa', 'Auxiliary Services', '2023', 'May', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(76, 'Lipa', 'RGO', '2022', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(77, 'Lipa', 'RGO', '2022', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(78, 'Lemery', 'RGO', '2024', 'September', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(79, 'Lipa', 'RGO', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(80, 'Lipa', 'RGO', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(81, 'Lemery', 'Procurement', '2022', 'February', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(82, 'Lemery', 'Procurement', '2022', 'February', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(83, 'Central', 'Procurement', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(84, 'Central', 'Procurement', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(85, 'ARASOF-Nasugbu', 'Procurement', '2022', 'September', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(86, 'ARASOF-Nasugbu', 'Procurement', '2022', 'September', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(87, 'Lipa', 'Procurement', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(88, 'Lipa', 'Procurement', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(89, 'Lipa', 'RGO', '2024', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(90, 'Lipa', 'RGO', '2024', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(91, 'Lipa', 'Auxiliary Services', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(92, 'Lipa', 'Auxiliary Services', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(93, 'Lipa', 'RGO', '2022', 'July', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(94, 'Lipa', 'RGO', '2022', 'July', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(95, 'Lemery', 'Procurement', '2022', 'October', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(96, 'JPLPC-Malvar', 'Auxiliary Services', '2022', 'January', 'Diesel', 12, '50', '98', '1176', '147.89749999999998', '0.1478975'),
(97, 'Lipa', 'Procurement', '2022', 'July', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(98, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Diesel', 10, '18', '35.28', '352.8', '53.2431', '0.0532431'),
(99, 'ARASOF-Nasugbu', 'Procurement', '2022', 'October', 'Diesel', 120, '10', '19.6', '2352', '29.5795', '0.029579499999999998'),
(100, 'Lipa', 'Procurement', '2023', 'December', 'Fuel', 25, '0', '0', '0', '0', '0'),
(101, 'Lipa', 'Auxiliary Services', '2024', 'December', 'Fuel', 10, '10', '19.6', '196', '29.5795', '0.029579499999999998'),
(102, 'Lipa', 'RGO', '2023', 'May', 'Diesel', 15, '10', '19.6', '294', '29.5795', '0.029579499999999998'),
(103, 'Lipa', 'Procurement', '2023', 'December', 'Diesel', 25, '30', '58.8', '1470', '88.7385', '0.0887385'),
(105, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 25, '15', '29.4', '735', '44.36925', '0.04436925'),
(106, 'Lipa', 'Auxiliary Services', '2023', 'November', 'Fuel', 25, '10', '19.6', '490.00000000000006', '29.5795', '0.029579499999999998'),
(107, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 15, '15', '29.4', '441', '44.36925', '0.04436925'),
(108, 'Lipa', 'Auxiliary Services', '2023', 'November', 'Fuel', 50, '30', '58.8', '2940', '88.7385', '0.0887385'),
(109, 'Lipa', 'Auxiliary Services', '2023', 'September', 'Fuel', 12, '120', '235.2', '2822.3999999999996', '354.954', '0.354954'),
(110, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Fuel', 10, '100', '196', '1960', '295.79499999999996', '0.295795'),
(111, 'Lipa', 'Procurement', '2022', 'June', 'Fuel', 5, '50', '98', '490', '147.89749999999998', '0.1478975'),
(112, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Fuel', 8, '80', '156.8', '1254.4', '236.636', '0.23663599999999999'),
(113, 'Lipa', 'RGO', '2023', 'August', 'Diesel', 5, '25', '49', '245', '73.94874999999999', '0.07394875'),
(114, 'Lipa', 'RGO', '2023', 'August', 'Diesel', 5, '25', '49', '245', '73.94874999999999', '0.07394875'),
(115, 'Lipa', 'Auxiliary Services', '2024', 'March', 'Fuel', 25, '250', '490', '12250', '739.4875', '0.7394875'),
(116, 'Lipa', 'Auxiliary Services', '2022', 'December', 'Fuel', 1, '15', '29.4', '29.4', '44.36925', '0.04436925'),
(117, 'Lipa', 'Procurement', '2022', 'July', 'Fuel', 4, '60', '117.6', '470.4', '177.477', '0.177477'),
(118, 'Lipa', 'Procurement', '2023', 'July', 'Fuel', 5, '40', '78.4', '392', '118.318', '0.11831799999999999'),
(119, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 2, '30', '58.8', '117.6', '88.7385', '0.0887385'),
(120, 'Lipa', 'Auxiliary Services', '2023', 'July', 'Diesel', 5, '30', '58.8', '294', '88.7385', '0.0887385'),
(122, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 14, '140', '274.4', '3841.5999999999995', '414.113', '0.414113'),
(123, 'Lipa', 'Procurement', '2023', 'May', 'Fuel', 5, '50', '98', '490', '147.89749999999998', '0.1478975'),
(124, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 15, '150', '294', '4410', '443.6925', '0.4436925'),
(125, 'Lipa', 'Auxiliary Services', '2023', 'November', 'Fuel', 2, '25', '49', '98', '73.94874999999999', '0.07394875'),
(126, 'Lipa', 'RGO', '2022', 'October', 'Fuel', 12, '120', '235.2', '2822.3999999999996', '354.954', '0.354954'),
(127, 'Lipa', 'Auxiliary Services', '2023', 'October', 'Diesel', 14, '140', '274.4', '3841.5999999999995', '414.113', '0.414113'),
(128, 'Lipa', 'Auxiliary Services', '2022', 'December', 'Fuel', 2, '20', '39.2', '78.4', '59.159', '0.059158999999999996'),
(129, 'Lipa', 'Auxiliary Services', '2023', 'November', 'Fuel', 10, '15', '29.4', '294', '44.36925', '0.04436925'),
(130, 'Lipa', 'Auxiliary Services', '2022', 'November', 'Fuel', 5, '25', '49', '245', '73.94874999999999', '0.07394875'),
(131, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Fuel', 15, '150', '294', '4410', '443.6925', '0.4436925'),
(132, 'Lipa', 'Auxiliary Services', '2024', 'October', 'Fuel', 48, '480', '940.8', '45158.399999999994', '1419.816', '1.419816'),
(134, 'Lipa', 'Auxiliary Services', '2022', 'October', 'Fuel', 15, '250', '490', '7350', '739.4875', '0.7394875'),
(135, 'Balayan', 'Auxiliary Services', '2023', 'November', 'Fuel', 58, '65.0', '127.39999999999999', '7389.2', '192.26675', '0.19226675000000001');

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
(76, 'Lipa', 2024, 'Q1', 'January', 'biodegradable', 'BiodegradableFood Waste', 49, 30.7166, 0.0307166),
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
(239, 'Lipa', 2020, 'Q4', 'December', 'recyclable', 'RecyclableMixed Plastic', 2.59, 0.023051, 0.000023051);

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
(0, 'Alangilan', '2024', 'January', 'Mixed Municipal Solid Waste', 150, 100, 0.1, 66.6667, 0.00665, 0.00000665),
(5, 'Lipa', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 100, 0.1, 83.3333, 6.65, 0.00665),
(6, 'Lipa', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 100, 0.1, 83.3333, 6.65, 0.00665),
(7, 'Lipa', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 100, 0.1, 83.3333, 6.65, 0.00665),
(9, 'Mabini', '2023', 'December', 'Mixed Municipal Solid Waste', 50, 80, 0.08, 160, 5.32, 0.00532),
(10, 'Mabini', '2023', 'December', 'Mixed Municipal Solid Waste', 50, 80, 0.08, 160, 5.32, 0.00532),
(11, 'Mabini', '2023', 'December', 'Mixed Municipal Solid Waste', 50, 80, 0.08, 160, 5.32, 0.00532),
(16, 'Lipa', '2022', 'August', 'Mixed Municipal Solid Waste', 80, 120, 0.12, 150, 7.98, 0.00798),
(17, 'Lipa', '2022', 'August', 'Mixed Municipal Solid Waste', 80, 120, 0.12, 150, 7.98, 0.00798),
(18, 'Lipa', '2021', 'June', 'Mixed Municipal Solid Waste', 155, 5, 0.005, 3.22581, 0.3325, 0.0003325),
(19, 'Lipa', '2021', 'June', 'Mixed Municipal Solid Waste', 155, 5, 0.005, 3.22581, 0.3325, 0.0003325),
(20, 'ARASOF-Nasugbu', '2022', 'November', 'Mixed Municipal Solid Waste', 50, 10, 0.01, 20, 0.665, 0.000665),
(21, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(22, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(23, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(24, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(25, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(26, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(27, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(28, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(29, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(30, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(31, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(32, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(33, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(34, 'ARASOF-Nasugbu', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 10, 0.01, 8.33333, 0.665, 0.000665),
(35, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(36, 'Alangilan', '2022', 'September', 'Mixed Municipal Solid Waste', 50, 25, 0.025, 50, 1.6625, 0.0016625),
(37, 'Balayan', '2021', 'September', 'Mixed Municipal Solid Waste', 50, 50, 0.05, 100, 3.325, 0.003325),
(38, 'ARASOF-Nasugbu', '2022', 'September', 'Mixed Municipal Solid Waste', 50, 40, 0.04, 80, 2.66, 0.00266),
(39, 'Lipa', '2022', 'March', 'Mixed Municipal Solid Waste', 100, 50, 0.05, 50, 3.325, 0.003325),
(40, 'ARASOF-Nasugbu', '2022', 'September', 'Mixed Municipal Solid Waste', 10, 10, 0.01, 100, 0.665, 0.000665),
(41, 'ARASOF-Nasugbu', '2021', 'November', 'Mixed Municipal Solid Waste', 120, 20, 0.02, 16.6667, 1.33, 0.00133),
(42, 'JPLPC-Malvar', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 10, 0.01, 8.33333, 0.665, 0.000665),
(43, 'Lemery', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 10, 0.01, 8.33333, 0.665, 0.000665),
(45, 'Lemery', '2022', 'September', 'Mixed Municipal Solid Waste', 120, 10, 0.01, 8.33333, 0.665, 0.000665),
(47, 'Lipa', '2021', 'January', 'Mixed Municipal Solid Waste', 100, 12, 0.012, 12, 0.798, 0.000798),
(48, 'Alangilan', '2021', 'January', 'Mixed Municipal Solid Waste', 20, 5, 0.005, 25, 0.3325, 0.0003325),
(49, 'Lipa', '2022', 'January', 'Mixed Municipal Solid Waste', 10, 10, 0.01, 100, 0.665, 0.000665),
(50, 'Lipa', '2022', 'April', 'Mixed Municipal Solid Waste', 10, 10, 0.01, 100, 0.665, 0.000665),
(51, 'Lipa', '2023', 'March', 'Mixed Municipal Solid Waste', 50, 5, 0.005, 10, 0.3325, 0.0003325),
(52, 'Lipa', '2021', 'March', 'Mixed Municipal Solid Waste', 10, 10, 0.01, 100, 0.665, 0.000665),
(53, 'Lipa', '2022', 'March', 'Mixed Municipal Solid Waste', 15, 10, 0.01, 66.6667, 0.665, 0.000665),
(54, 'Lipa', '2022', 'March', 'Mixed Municipal Solid Waste', 10, 10, 0.01, 100, 0.665, 0.000665);

-- --------------------------------------------------------

--
-- Table structure for table `tbltreatedwater`
--

CREATE TABLE `tbltreatedwater` (
  `id` int(11) NOT NULL,
  `Campus` varchar(255) DEFAULT NULL,
  `Month` varchar(50) DEFAULT NULL,
  `TreatedWaterVolume` decimal(10,2) DEFAULT NULL,
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
(1, 'Alangilan', 'January', 360.00, 60.00, 300.00, 0.00, 81.60000, 0.08160),
(2, 'ARASOF-Nasugbu', 'October', 9603.00, 100.00, 9503.00, 2584.82, 2584.81600, 2.58482),
(3, 'ARASOF-Nasugbu', 'October', 9603.00, 100.00, 9503.00, 2584.82, 2584.81600, 2.58482),
(4, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(5, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(6, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(7, 'Central', 'December', 1266.00, 125.00, 1141.00, 310.35, 310.35200, 0.31035),
(8, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(9, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(10, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(11, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(12, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(13, 'ARASOF-Nasugbu', 'July', 1500.00, 113.00, 1387.00, 377.26, 377.26400, 0.37726),
(14, 'ARASOF-Nasugbu', 'September', 1258.00, 136.00, 1122.00, 305.18, 305.18400, 0.30518),
(15, 'Central', 'September', 9603.00, 100.00, 9503.00, 2584.82, 2584.81600, 2.58482),
(16, 'ARASOF-Nasugbu', 'December', 1250.00, 250.00, 1000.00, 272.00, 272.00000, 0.27200),
(17, 'ARASOF-Nasugbu', 'December', 1520.00, 20.00, 1500.00, 408.00, 408.00000, 0.40800),
(18, 'Lipa', 'June', 1540.00, 140.00, 1400.00, 380.80, 380.80000, 0.38080),
(19, 'Lemery', 'August', 1450.00, 450.00, 1000.00, 272.00, 272.00000, 0.27200),
(20, 'JPLPC-Malvar', 'September', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(21, 'JPLPC-Malvar', 'September', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(22, 'Lipa', 'September', 1200.00, 100.00, 1100.00, 299.20, 299.20000, 0.29920),
(23, 'ARASOF-Nasugbu', 'September', 1200.00, 1000.00, 200.00, 54.40, 54.40000, 0.05440),
(24, 'Lipa', 'June', 9603.00, 100.00, 9503.00, 2584.82, 2584.81600, 2.58482),
(25, 'JPLPC-Malvar', 'February', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(26, 'Balayan', 'December', 1200.00, 200.00, 1000.00, 272.00, 272.00000, 0.27200),
(27, 'Balayan', 'December', 1200.00, 200.00, 1000.00, 272.00, 272.00000, 0.27200),
(28, 'Balayan', 'October', 500.00, 250.00, 250.00, 68.00, 68.00000, 0.06800),
(29, 'Balayan', 'October', 500.00, 250.00, 250.00, 68.00, 68.00000, 0.06800),
(32, 'Alangilan', 'December', 120.00, 120.00, 0.00, 0.00, 0.00000, 0.00000),
(33, 'Alangilan', 'December', 120.00, 120.00, 0.00, 0.00, 0.00000, 0.00000),
(41, 'Lemery', 'October', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(42, 'Lemery', 'October', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(43, 'Central', 'September', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(44, 'Central', 'September', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(45, 'Lemery', 'October', 200.00, 100.00, 100.00, 27.20, 27.20000, 0.02720),
(46, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(47, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(48, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(49, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(50, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(51, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(52, 'Lipa', 'December', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(53, 'Lipa', 'March', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(54, 'Lipa', 'March', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(55, 'ARASOF-Nasugbu', 'September', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(56, 'ARASOF-Nasugbu', 'September', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(57, 'Lipa', 'December', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(58, 'Lipa', 'December', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(59, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(60, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(62, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(63, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(64, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(65, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(66, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(67, 'Balayan', 'October', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(68, 'ARASOF-Nasugbu', 'September', 240.00, 40.00, 200.00, 54.40, 54.40000, 0.05440),
(69, 'ARASOF-Nasugbu', 'September', 240.00, 40.00, 200.00, 54.40, 54.40000, 0.05440),
(70, 'Balayan', 'March', 148.00, 100.00, 48.00, 13.06, 13.05600, 0.01306),
(71, 'Balayan', 'March', 148.00, 100.00, 48.00, 13.06, 13.05600, 0.01306),
(72, 'Balayan', 'March', 148.00, 100.00, 48.00, 13.06, 13.05600, 0.01306),
(73, 'Lipa', 'December', 120.00, 20.00, 100.00, 27.20, 27.20000, 0.02720),
(74, 'Lipa', 'March', 100.00, 100.00, 0.00, 0.00, 0.00000, 0.00000),
(76, 'Lipa', 'February', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(77, 'Lipa', 'March', 1000.00, 200.00, 800.00, 217.60, 217.60000, 0.21760),
(78, 'Lipa', 'June', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(79, 'Lipa', 'June', 250.00, 50.00, 200.00, 54.40, 54.40000, 0.05440),
(80, 'Lipa', 'March', 150.00, 50.00, 100.00, 27.20, 27.20000, 0.02720),
(81, 'Lipa', 'April', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(82, 'Lipa', 'July', 200.00, 90.00, 110.00, 29.92, 29.92000, 0.02992),
(83, 'Lipa', 'June', 150.00, 50.00, 100.00, 27.20, 27.20000, 0.02720),
(84, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(85, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(86, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(87, 'Lipa', 'February', 148.00, 100.00, 48.00, 13.06, 13.05600, 0.01306),
(88, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(89, 'Lipa', 'August', 100.00, 75.00, 25.00, 6.80, 6.80000, 0.00680),
(90, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(91, 'Lipa', 'September', 280.00, 140.00, 140.00, 38.08, 38.08000, 0.03808),
(92, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(93, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(94, 'Lipa', 'March', 140.00, 50.00, 90.00, 24.48, 24.48000, 0.02448),
(95, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(96, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(97, 'Lipa', 'April', 120.00, 50.00, 70.00, 19.04, 19.04000, 0.01904),
(98, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(99, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(100, 'Lipa', 'April', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(102, 'Lipa', 'September', 143.00, 75.00, 68.00, 18.50, 18.49600, 0.01850),
(103, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(104, 'Lipa', 'November', 180.00, 100.00, 80.00, 21.76, 21.76000, 0.02176),
(105, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(106, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(107, 'Lipa', 'June', 195.00, 150.00, 45.00, 12.24, 12.24000, 0.01224),
(108, 'Lipa', 'June', 400.00, 250.00, 150.00, 40.80, 40.80000, 0.04080),
(112, 'Lipa', 'July', 25.00, 10.00, 15.00, 4.08, 4.08000, 0.00408),
(113, 'Lipa', 'March', 120.00, 100.00, 20.00, 5.44, 5.44000, 0.00544),
(114, 'Lipa', 'January', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(115, 'Lipa', 'June', 150.00, 100.00, 50.00, 13.60, 13.60000, 0.01360),
(116, 'Lipa', 'April', 250.00, 150.00, 100.00, 27.20, 27.20000, 0.02720),
(117, 'Lipa', 'April', 150.00, 80.00, 70.00, 19.04, 19.04000, 0.01904),
(118, 'Lipa', 'December', 850.00, 50.00, 800.00, 217.60, 217.60000, 0.21760),
(119, 'Lipa', 'March', 250.00, 125.00, 125.00, 34.00, 34.00000, 0.03400),
(120, 'Lipa', 'June', 520.00, 400.00, 120.00, 32.64, 32.64000, 0.03264),
(121, 'Alangilan', 'February', 360.00, 60.00, 300.00, 0.00, 81.60000, 0.08160),
(125, 'Alangilan', 'May', 250.00, 125.00, 125.00, 34.00, 34.00000, 0.03400),
(126, 'Alangilan', 'January', 620.00, 120.00, 500.00, 136.00, 136.00000, 0.13600),
(127, 'Alangilan', 'January', 5131.00, 1245.00, 3886.00, 1056.99, 1056.99200, 1.05699),
(128, 'Alangilan', 'January', 6541.00, 1256.00, 5285.00, 1437.52, 1437.52000, 1.43752);

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
  `Consumption` decimal(10,2) DEFAULT NULL,
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
(174, 'JPLPC-Malvar', '2024-10-03', 'Deep Well', 150.00, 160.00, 250.00, 150.00, 0.60, 3.72500, 0.00373);

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
-- Indexes for table `tblcampus`
--
ALTER TABLE `tblcampus`
  ADD PRIMARY KEY (`Campus`);

--
-- Indexes for table `tblelectricity`
--
ALTER TABLE `tblelectricity`
  ADD KEY `Campus` (`Campus`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=177;

--
-- AUTO_INCREMENT for table `fuel_emissions`
--
ALTER TABLE `fuel_emissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=188;

--
-- AUTO_INCREMENT for table `tblaccommodation`
--
ALTER TABLE `tblaccommodation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT for table `tblflight`
--
ALTER TABLE `tblflight`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `tblfoodwaste`
--
ALTER TABLE `tblfoodwaste`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT for table `tbllpg`
--
ALTER TABLE `tbllpg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=136;

--
-- AUTO_INCREMENT for table `tblsolidwastesegregated`
--
ALTER TABLE `tblsolidwastesegregated`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=240;

--
-- AUTO_INCREMENT for table `tbltreatedwater`
--
ALTER TABLE `tbltreatedwater`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `tblwater`
--
ALTER TABLE `tblwater`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=176;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
