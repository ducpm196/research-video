CREATE VIEW WFG AS SELECT w.tx AS u, h.tx AS v FROM Wait w JOIN Held h ON w.r=h.r WHERE w.tx<>h.tx;
SELECT 'wait_edges=' || COUNT(*) FROM WFG;
WITH RECURSIVE r(s, c, d) AS (SELECT u, v, 1 FROM WFG UNION ALL SELECT s, w.v, d+1 FROM r JOIN WFG w ON r.c=w.u WHERE d<8) SELECT 'deadlock_detected=' || EXISTS(SELECT 1 FROM r WHERE s=c);
WITH RECURSIVE r(s, c, d) AS (SELECT u, v, 1 FROM WFG UNION ALL SELECT s, w.v, d+1 FROM r JOIN WFG w ON r.c=w.u WHERE d<8) SELECT 'victim_needed=' || EXISTS(SELECT 1 FROM r WHERE s=c);
