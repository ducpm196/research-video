CREATE TABLE TK(id TEXT PRIMARY KEY, sd INT CHECK(sd >= 0));
INSERT INTO TK VALUES ('A',100),('B',50);
BEGIN; UPDATE TK SET sd=sd-40 WHERE id='A'; UPDATE TK SET sd=sd+40 WHERE id='B'; COMMIT;
SELECT 'after_commit=' || GROUP_CONCAT(id||':'||sd, ',') FROM (SELECT id,sd FROM TK ORDER BY id);
BEGIN; UPDATE TK SET sd=sd-20 WHERE id='A'; ROLLBACK;
SELECT 'after_rollback=' || GROUP_CONCAT(id||':'||sd, ',') FROM (SELECT id,sd FROM TK ORDER BY id);
SELECT 'total_preserved=' || SUM(sd) FROM TK;
