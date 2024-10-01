CREATE DATABASE IF NOT EXISTS `whatsfeed`;
CREATE USER IF NOT EXISTS 'cederic' @'172.24.0.1' IDENTIFIED BY 'complicated';
CREATE USER IF NOT EXISTS 'cederic' @'172.24.0.3' IDENTIFIED BY 'complicated';
GRANT ALL PRIVILEGES ON whatsfeed.* TO 'cederic' @'172.24.0.1';
GRANT ALL PRIVILEGES ON whatsfeed.* TO 'cederic' @'172.24.0.3';
FLUSH PRIVILEGES;
USE `whatsfeed`;
CREATE TABLE IF NOT EXISTS `users` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `contact_name` varchar(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `pictures` (
    `image_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `picture_filename` varchar(255) NOT NULL,
    `timestamp` BIGINT NOT NULL,
    `user_id` int(11) NOT NULL,
    UNIQUE (`picture_filename`, `timestamp`, `user_id`),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS `status` (
    `status_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `status` varchar(255) NOT NULL,
    `timestamp` BIGINT NOT NULL,
    `user_id` int(11) NOT NULL,
    UNIQUE (`status`, `timestamp`, `user_id`),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);