CREATE DATABASE IF NOT EXISTS airpollution CHARACTER SET UTF8;
CREATE USER IF NOT EXISTS djangoadmin@localhost IDENTIFIED BY 'fenixarizona';
GRANT ALL PRIVILEGES ON airpollution.* to djangoadmin@localhost;
FLUSH PRIVILEGES;
