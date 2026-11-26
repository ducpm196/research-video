CREATE TABLE Lop(ma TEXT PRIMARY KEY, ten TEXT);
INSERT INTO Lop VALUES ('K1','CS'),('K2','AI'),('K3','SE');
CREATE TABLE SV(id INT, ten TEXT, lop TEXT, diem INT);
INSERT INTO SV VALUES (1,'Binh','K1',9),(2,'Cuong','K2',8),(3,'Dung',NULL,6),(4,'Hoa','K1',8),(5,'Lan','K3',10);
