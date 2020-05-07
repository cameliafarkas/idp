create database IF NOT EXISTS hairshop;

use hairshop;

DELIMITER //

CREATE TABLE IF NOT EXISTS product(
    id varchar(30) PRIMARY KEY,
    name varchar(40) NOT NULL,
    type varchar(30),
    in_stock int NOT NULL,
    company varchar(40) NOT NULL,
    price int NOT NULL
);

CREATE TABLE IF NOT EXISTS stock(
    id int PRIMARY KEY AUTO_INCREMENT,
    product_id varchar(30),
    quantity int DEFAULT 0,
    location_id varchar(30) DEFAULT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
    ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS shoppingcart(
    user varchar(30) PRIMARY KEY,
    delivery_cost int DEFAULT 15
);

CREATE TABLE IF NOT EXISTS cart_item(
    id int PRIMARY KEY AUTO_INCREMENT,
    id_product varchar(30),
    id_shoppingcart varchar(30),
    FOREIGN KEY (id_product) REFERENCES product(id)
    ON DELETE CASCADE,
    FOREIGN KEY (id_shoppingcart) REFERENCES shoppingcart(user)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pay(
    id int PRIMARY KEY AUTO_INCREMENT,
    cart_id varchar(30),
    name varchar(40),
    name_card varchar(40),
    email varchar(40),
    address varchar(50),
    card_number varchar(16),
    year year(4),
    cvv varchar(3),
    value int(11)
);



CREATE TRIGGER after_updating_stock
    AFTER UPDATE
    ON stock FOR EACH ROW
BEGIN
    IF quantity <= 0 THEN
        UPDATE PRODUCT
        SET in_stock = 0
        WHERE product_id = product.id;
    END IF;
END//
