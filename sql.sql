create database hyotaedb;

use hyotaedb;

drop table login;
drop table images;

CREATE TABLE login (
  id varchar(100) not null,
  password varchar(100) NOT NULL,
  name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
)charset=utf8;

CREATE TABLE images (
    title VARCHAR(100),
    text VARCHAR(100),
    data LONGBLOB,
    PRIMARY KEY (title)
)charset=utf8;