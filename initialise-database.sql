create database tasklist;
create user 'tasklist'@'localhost' identified with mysql_native_password by 'pirple';
grant all privileges on tasklist.* to 'tasklist'@'localhost';