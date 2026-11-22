CREATE TABLE Gia(id INT PRIMARY KEY, v INT); INSERT INTO Gia VALUES (1, 100);
BEGIN; UPDATE Gia SET v=200; SAVEPOINT s1; UPDATE Gia SET v=300; ROLLBACK TO s1;
SELECT 'after_s1_rollback=' || v FROM Gia;
ROLLBACK;
SELECT 'after_full_rollback=' || v FROM Gia;
SELECT 'dirty_read_prevented=' || (v = 100) FROM Gia;
