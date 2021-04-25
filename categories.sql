-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 25, 2021 at 04:49 AM
-- Server version: 8.0.18
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `braindb`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `category_description` text COLLATE utf8mb4_general_ci,
  `parent_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`, `category_description`, `parent_category`) VALUES
(1, 'Education', NULL, NULL),
(3, 'Public', NULL, 1),
(4, 'Private', NULL, 1),
(5, 'Home', NULL, 1),
(6, 'Geography', NULL, NULL),
(7, 'Religion', NULL, NULL),
(8, 'Science', NULL, NULL),
(9, 'Continents', NULL, 6),
(10, 'Catholicism', NULL, 7),
(11, 'Biology', NULL, 8),
(12, 'North America', NULL, 9),
(13, 'Churches', NULL, 10),
(14, 'Anatomy', NULL, 11),
(15, 'Space', NULL, NULL),
(16, 'Space shuttle', NULL, 15),
(17, 'Buddhism', NULL, 7),
(18, 'Roman catholic', NULL, 10),
(19, 'Human anatomy', NULL, 11),
(20, 'Art', NULL, NULL),
(21, 'Literature', NULL, 20),
(22, 'Autobiography', NULL, 21),
(23, 'Music', NULL, NULL),
(24, 'Weather', NULL, NULL),
(25, 'Storms', NULL, 24),
(26, 'Hurricane', NULL, 25),
(27, 'Mid-western', NULL, 24),
(28, 'Puzzles', NULL, NULL),
(29, 'Jigsaw', NULL, 28),
(30, 'Large', NULL, 29),
(31, 'Law', NULL, NULL),
(32, 'Cell phones', NULL, NULL),
(33, 'Apple', NULL, 32),
(34, 'Iphone', NULL, 33);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`),
  ADD UNIQUE KEY `category_name` (`category_name`),
  ADD KEY `parent_category` (`parent_category`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_category`) REFERENCES `categories` (`category_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
