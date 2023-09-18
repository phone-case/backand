# server

### !pip install flask

create database hyotaedb;

use hyotaedb;

CREATE TABLE test (
  id varchar(8) not null,
  password varchar(8) NOT NULL,
  name varchar(20) DEFAULT NULL,
  role varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;