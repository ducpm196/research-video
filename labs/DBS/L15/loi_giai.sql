BEGIN;
UPDATE Gia SET v=(SELECT v1 FROM Params);
SAVEPOINT s1;
UPDATE Gia SET v=(SELECT v2 FROM Params);
ROLLBACK TO s1;
SELECT 'after_s1_rollback=' || v FROM Gia;
ROLLBACK;
SELECT 'after_full_rollback=' || v FROM Gia;
SELECT 'dirty_read_prevented=' || (v = (SELECT v0 FROM Params)) FROM Gia;
