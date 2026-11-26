SELECT 'rows=' || COUNT(*) || ' distinct_ad=' || COUNT(DISTINCT A||'-'||D) FROM R;
SELECT 'a_not_unique=' || (COUNT(*) > COUNT(DISTINCT A)) FROM R;
SELECT 'fd_a_to_b_holds=' || (NOT EXISTS(SELECT 1 FROM R x JOIN R y ON x.A=y.A AND x.B<>y.B));
