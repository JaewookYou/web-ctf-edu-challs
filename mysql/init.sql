SET collation_connection = 'utf8_general_ci';

#drop database fsi;
create database fsi;
ALTER DATABASE fsi CHARACTER SET utf8 COLLATE utf8_general_ci;

use fsi;

#drop table sqli1_table;

create user 'sqli1'@'%' identified by '[REDACTED]';
create user 'sqli2'@'%' identified by '[REDACTED]';
create user 'sqli3'@'%' identified by '[REDACTED]';

create table sqli1_table(
	userseq int not null auto_increment primary key,
	userid varchar(50) not null, 
	userpw varchar(255) not null
);

create table sqli2_table(
	userseq int not null auto_increment primary key,
	userid varchar(50) not null, 
	userpw varchar(255) not null
);

create table sqli3_table(
	userseq int not null auto_increment primary key,
	userid varchar(50) not null, 
	userpw varchar(255) not null
);


ALTER TABLE sqli1_table CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE sqli2_table CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE sqli3_table CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

insert into sqli1_table (userid, userpw) values ("guest","guest"), ("admin", "[REDACTED]"); 
insert into sqli2_table (userid, userpw) values ("guest","guest"), ("admin", "[REDACTED]"); 
insert into sqli3_table (userid, userpw) values ("guest","guest"), ("admin", "flag{[REDACTED]}"); 

grant select on fsi.sqli1_table to 'sqli1'@'%';
grant select on fsi.sqli2_table to 'sqli2'@'%';
grant select on fsi.sqli3_table to 'sqli3'@'%';


flush privileges;