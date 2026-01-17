--
-- Create model Cart
--
CREATE TABLE `cart_cart` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `created_at` datetime(6) NOT NULL, `customer_id` bigint NOT NULL UNIQUE);
--
-- Create model CartItem
--
CREATE TABLE `cart_cartitem` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `quantity` integer NOT NULL, `book_id` bigint NOT NULL, `cart_id` bigint NOT NULL);
ALTER TABLE `cart_cart` ADD CONSTRAINT `cart_cart_customer_id_bbe4c408_fk_accounts_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `accounts_customer` (`id`);
ALTER TABLE `cart_cartitem` ADD CONSTRAINT `cart_cartitem_book_id_7dc5504d_fk_books_book_id` FOREIGN KEY (`book_id`) REFERENCES `books_book` (`id`);
ALTER TABLE `cart_cartitem` ADD CONSTRAINT `cart_cartitem_cart_id_370ad265_fk_cart_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`);
