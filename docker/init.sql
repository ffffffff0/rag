CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'rag';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS rag;
USE rag;