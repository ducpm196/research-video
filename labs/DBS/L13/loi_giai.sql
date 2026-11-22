CREATE TABLE Held(r TEXT, tx INT); INSERT INTO Held VALUES ('A',1),('B',2);
CREATE TABLE Wait(tx INT, r TEXT); INSERT INTO Wait VALUES (1,'B'),(2,'A');
CREATE VIEW WFG AS SELECT w.tx AS u, h.tx AS v FROM Wait w JOIN Held h ON w.r=h.r WHERE w.tx<>h.tx;
SELECT 'wait_edges=' || COUNT(*) FROM WFG;
SELECT 'deadlock_detected=' || EXISTS(SELECT 1 FROM WFG a JOIN WFG b ON a.v=b.u AND b.v=a.u);
SELECT 'victim_needed=' || EXISTS(SELECT 1 FROM WFG a JOIN WFG b ON a.v=b.u AND b.v=a.u);
