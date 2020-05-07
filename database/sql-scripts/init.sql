create database IF NOT EXISTS hairshop;

use hairshop;
SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `cart_item`;
CREATE TABLE `cart_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_product` varchar(30) DEFAULT NULL,
  `id_shoppingcart` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_product` (`id_product`),
  KEY `id_shoppingcart` (`id_shoppingcart`),
  CONSTRAINT `cart_item_ibfk_1` FOREIGN KEY (`id_product`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cart_item_ibfk_2` FOREIGN KEY (`id_shoppingcart`) REFERENCES `shoppingcart` (`user`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `pay`;
CREATE TABLE `pay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` varchar(30) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `name_card` varchar(40) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `card_number` varchar(16) DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  `cvv` varchar(3) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `in_stock` int(11) NOT NULL,
  `company` varchar(40) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `product` (`id`, `name`, `type`, `in_stock`, `company`, `price`) VALUES
('1',	'Oxidant 1.9%',	'vopsele-oxidanti',	1,	'Wella',	109),
('2121',	'Colour refresh pink pop',	'vopsele-oxidanti',	1,	'Maria Nila',	90),
('21D',	'Vopsea permanenta Bronze Ruby',	'vopsele-oxidanti',	1,	'L\'oreal',	45),
('23456',	'Sampon uscat',	'ingrijire',	1,	'Alama',	50),
('2391',	'Colour refresh autumn red',	'vopsele-oxidanti',	1,	'Maria Nila',	90),
('492',	'Ulei de par gel',	'styling',	1,	'L\'oreal',	49),
('4I30',	'Spuma definire bucle',	'styling',	1,	'Wella',	38),
('4kem',	'Spuma cu efect antistatic',	'styling',	1,	'Wella',	38),
('566ed',	'Emulsie oxidanta',	'vopsele-oxidanti',	1,	'Oro del Marocco',	121),
('56782',	'Deodorant aloe vera',	'ingrijire',	1,	'Aphrodite',	25),
('5798',	'Ulei ingrijire par vopsit',	'ingrijire',	1,	'Oro del Marocco',	125),
('78954',	'Lotiune de fixare a stralucirii',	'styling',	1,	'Wella',	75),
('789e',	'Balsam nutritiv pentru ingrijire',	'ingrijire',	1,	'Wella',	100),
('904ids',	'Spray proteic',	'ingrijire',	1,	'Oro di luce',	120),
('S4439',	'Vopsea semipermanenta midnight blue',	'vopsele-oxidanti',	1,	'Directions',	58),
('w3de',	'Spray ingrijire',	'ingrijire',	1,	'Kerastase',	48);

DROP TABLE IF EXISTS `shoppingcart`;
CREATE TABLE `shoppingcart` (
  `user` varchar(30) NOT NULL,
  `delivery_cost` int(11) DEFAULT '15',
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `shoppingcart` (`user`, `delivery_cost`) VALUES
('aaaaa',	15);

DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` varchar(30) DEFAULT NULL,
  `quantity` int(11) DEFAULT '0',
  `location_id` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `stock` (`id`, `product_id`, `quantity`, `location_id`) VALUES
(1,	'1',	123,	NULL),
(2,	'2121',	221,	NULL),
(3,	'21D',	121,	NULL),
(4,	'23456',	532,	NULL),
(5,	'2391',	322,	NULL),
(6,	'492',	532,	NULL),
(7,	'4I30',	122,	NULL),
(8,	'4kem',	421,	NULL),
(9,	'566ed',	456,	NULL),
(10,	'56782',	432,	NULL),
(11,	'5798',	135,	NULL),
(12,	'78954',	567,	NULL),
(13,	'789e',	234,	NULL),
(14,	'904ids',	54773,	NULL),
(15,	'S4439',	8473,	NULL),
(16,	'w3de',	2373,	NULL);

DELIMITER ;;

CREATE TRIGGER `after_updating_stock` AFTER UPDATE ON `stock` FOR EACH ROW
BEGIN
    IF quantity <= 0 THEN
        UPDATE PRODUCT
        SET in_stock = 0
        WHERE product_id = product.id;
    END IF;
END;;

DELIMITER ;
