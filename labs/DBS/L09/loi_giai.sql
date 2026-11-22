CREATE TABLE Diem(id INT, lop TEXT, diem INT);
INSERT INTO Diem VALUES (1,'K1',8),(2,'K1',9),(3,'K2',7),(4,'K2',8),(5,'K1',5);
CREATE INDEX idx_ld ON Diem(lop, diem);
SELECT 'composite_idx_ok=' || COUNT(*) FROM sqlite_master WHERE name='idx_ld';
SELECT 'k1_ge8=' || COUNT(*) FROM Diem WHERE lop='K1' AND diem >= 8;
SELECT 'between_7_9=' || COUNT(*) FROM Diem WHERE diem BETWEEN 7 AND 9;
