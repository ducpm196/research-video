SELECT 'friend_of_friend=' || b.v FROM Ban a JOIN Ban b ON a.v=b.u WHERE a.u='S1' ORDER BY b.v LIMIT 1;
SELECT 'json_role=' || json_extract(doc, '$.role') FROM Meta LIMIT 1;
SELECT 'nosql_fit=graph_doc';
