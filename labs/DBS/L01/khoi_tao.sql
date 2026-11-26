CREATE TABLE Lop(ma TEXT PRIMARY KEY, ten TEXT);
INSERT INTO Lop VALUES ('K1','CS'),('K2','AI');
CREATE TABLE SV(id INT, ten TEXT, lop TEXT, diem INT);
INSERT INTO SV VALUES (1,'An','K1',8),(2,'Binh','K1',6),(3,'Chi','K2',9),(4,'Dung',NULL,7);
