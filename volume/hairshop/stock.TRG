TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER after_updating_stock\n    AFTER UPDATE\n    ON stock FOR EACH ROW\nBEGIN\n    IF quantity <= 0 THEN\n        UPDATE PRODUCT\n        SET in_stock = 0\n        WHERE product_id = product.id;\n    END IF;\nEND'
sql_modes=1073741824
definers='root@localhost'
client_cs_names='latin1'
connection_cl_names='latin1_swedish_ci'
db_cl_names='latin1_swedish_ci'
