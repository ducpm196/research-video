CREATE TABLE Held(r TEXT, tx INT);
INSERT INTO Held VALUES ('A',1),('B',2),('C',3);
CREATE TABLE Wait(tx INT, r TEXT);
INSERT INTO Wait VALUES (1,'B'),(2,'C'),(3,'A');
