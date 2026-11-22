CREATE TABLE Edges(u INT, v INT); INSERT INTO Edges VALUES (1, 2), (2, 1);
SELECT 'edges=' || COUNT(*) FROM Edges;
WITH RECURSIVE reach(s, c, d) AS (SELECT u, v, 1 FROM Edges UNION ALL SELECT s, e.v, d+1 FROM reach r JOIN Edges e ON r.c=e.u WHERE d<5) SELECT 'cycle_found=' || EXISTS(SELECT 1 FROM reach WHERE s=c);
WITH RECURSIVE reach(s, c, d) AS (SELECT u, v, 1 FROM Edges UNION ALL SELECT s, e.v, d+1 FROM reach r JOIN Edges e ON r.c=e.u WHERE d<5) SELECT 'conflict_serializable=' || (NOT EXISTS(SELECT 1 FROM reach WHERE s=c));
