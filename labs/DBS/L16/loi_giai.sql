CREATE TABLE Ban(u TEXT, v TEXT); INSERT INTO Ban VALUES ('S1','S2'),('S2','S3');
SELECT 'friend_of_friend=' || b.v FROM Ban a JOIN Ban b ON a.v=b.u WHERE a.u='S1';
SELECT 'json_role=' || json_extract('{"role":"ai","tier":2}', '$.role');
SELECT 'nosql_fit=graph_doc';
