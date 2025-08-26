-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 26, 2025 at 04:19 AM
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
-- Database: `e-commerce-web`
--

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `status` enum('pending','paid','shipped','completed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `image`, `created_at`) VALUES
(2, 'Black Shirt', 'sadasd', 599, 34, 'black_shirt.jpg', '2025-08-21 04:45:16'),
(3, 'Luffy Tshirt', 'luffy designed shirt', 549, 10, 'luffy.png', '2025-08-26 01:40:57'),
(4, 'White Shirt', 'white basketball shirt', 499, 12, 'white_shirt.jpg', '2025-08-26 01:49:38'),
(5, 'Goku Black Shirt', 'Goku Dragon Ball character', 699, 16, 'dragon_ball.jpg', '2025-08-26 01:59:52'),
(6, 'Power Supply Shirt', 'white shirt P', 499, 11, 'Powers_Supply.jpg', '2025-08-26 02:17:01');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` enum('admin','user') NOT NULL DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `firstname`, `lastname`, `username`, `password`, `is_admin`, `created_at`) VALUES
(2, 'jaymar', 'roco', 'admin44', 'scrypt:32768:8:1$G6jR3JvpRuCHlucr$aac5963ebc4b5fabe2a971af9aaf54c41f7e44691c838ac7014ae2a1750ad4e0cf168bccadc00271c91d1546ad1057b325504e588f8ef390ba89d4f8dde38834', 'admin', '2025-08-20 02:53:24'),
(3, 'assdsassd', 'asdsasdd', 'asdasd', 'scrypt:32768:8:1$bUgxocxiAjvOwKuI$efbea6d38990a3079a882f5964b263516453d00bc667e22bcb6d23bda9c851f257ed32920ca6e01629dd0292340bb4d7c6647baa8bd5730f17be40e5bb1444c1', 'user', '2025-08-20 02:55:19'),
(4, 'admin23', 'admin23', 'admin23', 'scrypt:32768:8:1$DubnimO0cmmgJ6NW$361a2e8d52c473d6da10922ae8ccd9738572aa9e84e9fbc80b67cf0358e9f08527e6a8001494f77c82793978481e77c7f065e872243ff6e8fb350e0092cd76eb', 'admin', '2025-08-20 04:49:31'),
(7, 'asdasd', 'adsad', 'adsdasd@asd', 'scrypt:32768:8:1$THcQ502TD6ZLAMWL$d830e861811aaa76c501b63efecc43df179c4bbee89a66d283f8f80fee3dfddc1833007f763a58c2605eb112d975d59670c5a4852cfb0635d36d5eaec7ad8d35', 'admin', '2025-08-20 23:16:36'),
(9, 'asdasd', 'adsad', 'adsdasd@asdsssss', 'scrypt:32768:8:1$eeW4wNUaaTKBwHkg$409d347da0220fea476c0513c98571bdde202cc49348401ec9fdf06edd438cce0c7219b69591036234b918b7813bc11d156400b523e5d8e23ab63d202ef63837', 'admin', '2025-08-20 23:20:59'),
(10, 'admin16', 'admin', 'admin@admin', 'scrypt:32768:8:1$jvDZ4MrCBU38H7Um$9beef15730cb5c299fe7bf3f0df2abe7452168d33acd7e1ecbd25715897fd87f30695455e76a7ca8a8c8a709c37907945e2a1a39eea9b0c0bfc6aa52ac41168c', 'admin', '2025-08-21 03:09:16'),
(11, 'admin123', 'admin123', 'admin123@admin123', 'scrypt:32768:8:1$mV5Jyw5gBh66EGYn$d1bbeef7e73660ed118762d69120bb634d900d3679bba15ae0f36e3102aeb812175d9b75de82f8d1c9eeb5a388a8447bdccaf6e8b5f3d0890a3150e74ae39a67', 'admin', '2025-08-21 03:12:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
