CREATE TABLE ACCOUNTS( ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  T DATETIME, EMAIL TEXT,
  PASSWORD TEXT, UID INT,
  FOREIGN KEY(UID) REFERENCES USERS(ID)) AUTO_INCREMENT=1;
