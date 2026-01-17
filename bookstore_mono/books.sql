--
-- Create model Book
--
CREATE TABLE `books_book` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(200) NOT NULL, `author` varchar(100) NOT NULL, `price` numeric(10, 2) NOT NULL, `stock` integer NOT NULL);
