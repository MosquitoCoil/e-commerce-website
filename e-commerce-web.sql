-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 24, 2025 at 09:40 AM
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
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `size` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`, `created_at`, `size`) VALUES
(171, 17, 23, 1, '2025-09-22 04:56:28', 'L'),
(181, 2, 24, 1, '2025-09-23 04:11:56', 'L');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `status` enum('Pending','Processing','Delivered','Completed','Cancelled','Received') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `received_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total`, `status`, `created_at`, `received_at`) VALUES
(1, 4, 5041.00, 'Processing', '2025-08-31 11:30:39', NULL),
(2, 4, 4193.00, 'Processing', '2025-08-31 11:45:46', NULL),
(15, 2, 3244.00, 'Cancelled', '2025-09-01 07:58:15', NULL),
(17, 2, 3843.00, 'Received', '2025-09-01 09:29:45', NULL),
(18, 2, 3394.00, 'Received', '2025-09-01 09:57:47', NULL),
(19, 2, 3394.00, 'Completed', '2025-09-01 10:06:25', NULL),
(31, 2, 2945.00, 'Pending', '2025-09-01 10:39:35', NULL),
(32, 18, 3394.00, 'Completed', '2025-09-01 10:44:23', NULL),
(34, 18, 3394.00, 'Received', '2025-09-01 10:47:43', NULL),
(36, 18, 2346.00, 'Processing', '2025-09-01 10:53:07', NULL),
(39, 17, 1358.00, 'Pending', '2025-09-19 07:43:51', NULL),
(42, 17, 1295.00, 'Pending', '2025-09-19 09:39:31', NULL),
(43, 17, 998.00, 'Pending', '2025-09-20 01:10:15', NULL),
(44, 17, 499.00, 'Pending', '2025-09-20 01:13:10', NULL),
(45, 17, 499.00, 'Pending', '2025-09-20 01:22:17', NULL),
(46, 17, 499.00, 'Pending', '2025-09-20 01:33:44', NULL),
(49, 17, 499.00, 'Received', '2025-09-20 01:38:10', NULL),
(50, 19, 998.00, 'Received', '2025-09-22 05:38:09', NULL),
(52, 2, 499.00, 'Completed', '2025-09-23 04:11:10', NULL),
(57, 19, 1497.00, 'Cancelled', '2025-09-24 03:41:32', NULL),
(62, 19, 998.00, 'Pending', '2025-09-24 06:22:17', NULL),
(66, 19, 1497.00, 'Pending', '2025-09-24 06:29:45', NULL),
(67, 19, 1497.00, 'Received', '2025-09-24 06:39:05', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `size` varchar(50) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `size`, `quantity`, `price`) VALUES
(155, 50, 23, NULL, 1, 499.00),
(156, 50, 24, NULL, 1, 499.00),
(160, 52, 24, NULL, 1, 499.00),
(171, 57, 26, NULL, 1, 499.00),
(172, 57, 30, NULL, 1, 499.00),
(173, 57, 22, NULL, 1, 499.00),
(187, 62, 27, NULL, 1, 499.00),
(188, 62, 21, NULL, 1, 499.00),
(192, 66, 23, 'M', 2, 499.00),
(193, 66, 27, 'XXL', 1, 499.00),
(194, 67, 27, 'L', 2, 499.00),
(195, 67, 22, 'M', 1, 499.00);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `price` int(11) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `image`, `created_at`) VALUES
(21, 'Gray Shirt', '100% Cotton Shirt ', 499, 'gray-shirt.jpg', '2025-09-20 06:06:09'),
(22, 'Orange Shirt', '100% Cotton Shirt ', 499, 'orange-shirt.jpg', '2025-09-20 06:06:57'),
(23, 'Yellow Shirt', '100% Cotton Shirt ', 499, 'yellow-shirt.jpg', '2025-09-20 06:08:32'),
(24, 'Olive Green Shirt', '100% Cotton Shirt ', 499, 'olive-green-shirt.jpg', '2025-09-20 06:08:59'),
(25, 'Forest Green Shirt', '100% Cotton Shirt ', 499, 'forest-green-shirt.jpg', '2025-09-20 06:09:22'),
(26, 'Maroon Shirt', '100% Cotton Shirt ', 499, 'maroon-shirt.jpg', '2025-09-20 06:09:55'),
(27, 'Red Shirt', '100% Cotton Shirt ', 499, 'red-shirt.jpg', '2025-09-20 06:10:13'),
(28, 'Sky Blue Shirt', '100% Cotton Shirt ', 499, 'sky-blue-shirt.jpg', '2025-09-20 06:10:33'),
(29, 'Royal Blue Shirt', '100% Cotton Shirt ', 499, 'royal-blue-shirt.jpg', '2025-09-20 06:10:59'),
(30, 'Navy Blue Shirt', '100% Cotton Shirt ', 499, 'navy-blue-shirt.jpg', '2025-09-20 06:11:20'),
(31, 'White Shirt', '100% Cotton Shirt ', 499, 'white-shirt.jpg', '2025-09-20 06:11:41'),
(33, 'Black Shirt', '100% Cotton Shirt ', 499, 'black-shirt.jpg', '2025-09-20 06:14:21');

-- --------------------------------------------------------

--
-- Table structure for table `product_variants`
--

CREATE TABLE `product_variants` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `size` varchar(10) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_variants`
--

INSERT INTO `product_variants` (`id`, `product_id`, `size`, `stock`) VALUES
(13, 21, 'S', 12),
(14, 21, 'M', 8),
(15, 21, 'L', 15),
(16, 21, 'XL', 14),
(17, 21, 'XXL', 15),
(18, 22, 'S', 12),
(19, 22, 'M', 9),
(20, 22, 'L', 15),
(21, 22, 'XL', 12),
(22, 22, 'XXL', 15),
(23, 23, 'S', 10),
(24, 23, 'M', 7),
(25, 23, 'L', 10),
(26, 23, 'XL', 13),
(27, 23, 'XXL', 14),
(28, 24, 'S', 10),
(29, 24, 'M', 10),
(30, 24, 'L', 10),
(31, 24, 'XL', 12),
(32, 24, 'XXL', 14),
(33, 25, 'S', 10),
(34, 25, 'M', 11),
(35, 25, 'L', 12),
(36, 25, 'XL', 13),
(37, 25, 'XXL', 14),
(38, 26, 'S', 10),
(39, 26, 'M', 11),
(40, 26, 'L', 11),
(41, 26, 'XL', 13),
(42, 26, 'XXL', 14),
(43, 27, 'S', 10),
(44, 27, 'M', 9),
(45, 27, 'L', 9),
(46, 27, 'XL', 11),
(47, 27, 'XXL', 13),
(48, 28, 'S', 10),
(49, 28, 'M', 10),
(50, 28, 'L', 12),
(51, 28, 'XL', 13),
(52, 28, 'XXL', 14),
(53, 29, 'S', 10),
(54, 29, 'M', 11),
(55, 29, 'L', 12),
(56, 29, 'XL', 13),
(57, 29, 'XXL', 14),
(58, 30, 'S', 10),
(59, 30, 'M', 11),
(60, 30, 'L', 12),
(61, 30, 'XL', 12),
(62, 30, 'XXL', 14),
(63, 31, 'S', 10),
(64, 31, 'M', 11),
(65, 31, 'L', 12),
(66, 31, 'XL', 13),
(67, 31, 'XXL', 14),
(73, 33, 'S', 10),
(74, 33, 'M', 11),
(75, 33, 'L', 11),
(76, 33, 'XL', 13),
(77, 33, 'XXL', 14);

-- --------------------------------------------------------

--
-- Table structure for table `purchase_history`
--

CREATE TABLE `purchase_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `received_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase_history`
--

INSERT INTO `purchase_history` (`id`, `user_id`, `order_id`, `product_id`, `product_name`, `quantity`, `price`, `total`, `received_at`) VALUES
(1, 18, 34, NULL, 'Black shirt', 1, 599.00, 599.00, '2025-09-02 08:59:14'),
(2, 18, 34, NULL, 'Luffy Tshirt', 2, 549.00, 1098.00, '2025-09-02 08:59:14'),
(3, 18, 34, NULL, 'White Shirt', 2, 499.00, 998.00, '2025-09-02 08:59:14'),
(4, 18, 34, NULL, 'Goku Black Shirt', 1, 699.00, 699.00, '2025-09-02 08:59:14'),
(5, 19, 50, 23, 'Yellow Shirt', 1, 499.00, 499.00, '2025-09-22 13:39:11'),
(6, 19, 50, 24, 'Olive Green Shirt', 1, 499.00, 499.00, '2025-09-22 13:39:11'),
(7, 19, 57, 26, 'Maroon Shirt', 1, 499.00, 499.00, '2025-09-24 11:49:35'),
(8, 19, 57, 30, 'Navy Blue Shirt', 1, 499.00, 499.00, '2025-09-24 11:49:35'),
(10, 19, 67, 27, 'Red Shirt', 2, 499.00, 998.00, '2025-09-24 14:42:30');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` enum('admin','user') NOT NULL DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `firstname`, `lastname`, `address`, `username`, `password`, `is_admin`, `created_at`) VALUES
(2, 'jaymar', 'Roco', 'Happyland St.', 'admin44@admin44', 'scrypt:32768:8:1$VGEhaZSH5d82U3Nw$9b62c86aab50509add040ae3f2880014a24728dd7bdfbe816f7ceab2207d2b0d7be94a29f0f68424d43f5b40ed75ae7dc6cf1c881a887cb5657a701b3eafc376', 'admin', '2025-08-20 02:53:24'),
(4, 'admin23', 'admin23', NULL, 'admin23@admin23', 'scrypt:32768:8:1$tqS5ZPYsPW7Sye9B$c0ebeaf8e808414441274fcf2cd7460d857e6029d734cd604d5c1e38feb49277606199e74732a24563c45555fb557ffda51b3a2c994250a6da19bc596c207652', 'user', '2025-08-20 04:49:31'),
(7, 'asdasd', 'adsad', NULL, 'adsdasd@asd', 'scrypt:32768:8:1$THcQ502TD6ZLAMWL$d830e861811aaa76c501b63efecc43df179c4bbee89a66d283f8f80fee3dfddc1833007f763a58c2605eb112d975d59670c5a4852cfb0635d36d5eaec7ad8d35', 'user', '2025-08-20 23:16:36'),
(9, 'asdasd', 'adsad', NULL, 'adsdasd@asdsssss', 'scrypt:32768:8:1$eeW4wNUaaTKBwHkg$409d347da0220fea476c0513c98571bdde202cc49348401ec9fdf06edd438cce0c7219b69591036234b918b7813bc11d156400b523e5d8e23ab63d202ef63837', 'admin', '2025-08-20 23:20:59'),
(10, 'admin16', 'admin', NULL, 'admin@admin', 'scrypt:32768:8:1$jvDZ4MrCBU38H7Um$9beef15730cb5c299fe7bf3f0df2abe7452168d33acd7e1ecbd25715897fd87f30695455e76a7ca8a8c8a709c37907945e2a1a39eea9b0c0bfc6aa52ac41168c', 'admin', '2025-08-21 03:09:16'),
(11, 'admin123', 'admin123', NULL, 'admin123@admin123', 'scrypt:32768:8:1$mV5Jyw5gBh66EGYn$d1bbeef7e73660ed118762d69120bb634d900d3679bba15ae0f36e3102aeb812175d9b75de82f8d1c9eeb5a388a8447bdccaf6e8b5f3d0890a3150e74ae39a67', 'admin', '2025-08-21 03:12:02'),
(12, 'sadasd', 'asdasd', NULL, 'asdasd@asdasd', 'scrypt:32768:8:1$FJTAG4vKzZcpRyEE$ebc3be040ce4a19abae88d1150c43a4d22bac1ef64cc676e8c96dca3dc807c780a96a27dfed1c6036156cbba1283941a57a053cb711ab94f4357ac9913c38ccf', 'user', '2025-08-27 01:25:40'),
(13, 'client', 'client', NULL, 'client@client', 'scrypt:32768:8:1$6i3Rz5JdhfksmmZ4$8cf6afd82036ba52e4d21917abebc51a1a88f416f94d6c74bd30af8a86b95ad8c976865cab8d1b5d8e36b5c6adc5c2b5510bd6219c35dbc443b83cd385830bbc', 'user', '2025-08-27 01:27:10'),
(17, 'Client 1', 'client@23', 'Litex Rd. Commonwealth, Quezon City', 'client@23', 'scrypt:32768:8:1$X1RsmagYy4jBfyZl$cd376fabf94e3bf098a9ac788cc8c77b747b2502952396109f1cbfdf1a86df6b5adc3956631aa00b30bf51761ba41f8816990230863ffd3339828545fa212040', 'user', '2025-08-31 12:17:39'),
(18, 'client16', 'client16', 'Happyland St.', 'client@16', 'scrypt:32768:8:1$FYp8ZYyy96hWlYj7$ae2095291e994505a69c6e86cc43f2acf87afe354b9f75c214f4a675b3e4df076be53a9e7462e5d7000a908b009f472ebb181abbc3972b688f8622e0e570e590', 'user', '2025-09-01 10:44:11'),
(19, 'client@1', 'client@1', 'Litex Rd. Commonwealth, Quezon City', 'client@1', 'scrypt:32768:8:1$SjL9gliB3CBKqqaU$5ad8d9cc4ee7880724b5970c9c7ee9d6499a292d1e759700d74adc153bbb292f5d60d13ce7c1c013187e224f1acbe53e5464f33f96b7a6a0764421c4ec48abd9', 'user', '2025-09-22 05:37:49'),
(20, 'asda', 'sdasd', NULL, 'asdas@asdasd', 'scrypt:32768:8:1$c1yVY0PngUfsasky$10d8f5a13dce53e3f10c9805899bc176f994815e3eeec2cf92a6b75101b6eece42d5fd19934cc3f36cad4293e9aa09d3687881df57fbe7d06e0ed83b4f5231ea', 'user', '2025-09-22 08:47:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `fk_orderitems_product` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product_variants`
--
ALTER TABLE `product_variants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `purchase_history`
--
ALTER TABLE `purchase_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_purchase_user` (`user_id`),
  ADD KEY `fk_purchase_order` (`order_id`),
  ADD KEY `fk_purchase_product` (`product_id`);

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
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=221;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=196;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `product_variants`
--
ALTER TABLE `product_variants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT for table `purchase_history`
--
ALTER TABLE `purchase_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_orderitems_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `product_variants`
--
ALTER TABLE `product_variants`
  ADD CONSTRAINT `product_variants_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `purchase_history`
--
ALTER TABLE `purchase_history`
  ADD CONSTRAINT `fk_purchase_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_purchase_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_purchase_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
