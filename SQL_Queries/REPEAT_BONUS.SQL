create table REPEAT_BONUS (ID int not null auto_increment,NAME text,FREQUENCY int,UPPER_BOUND int, UID int,FOREIGN KEY (UID) REFERENCES USERS(ID), PRIMARY KEY (ID)) AUTO_INCREMENT = 1; 
