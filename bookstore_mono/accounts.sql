--
-- Create model Customer
--
CREATE TABLE `accounts_customer` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `email` varchar(254) NOT NULL UNIQUE, `password` varchar(255) NOT NULL);
