PRAGMA foreign_keys = ON;
INSERT OR IGNORE INTO DK SELECT mssv, ma, diem FROM NhapDK;
SELECT 'enrolled_rows=' || COUNT(*) FROM DK;
SELECT 'dup_enroll_blocked=' || ((SELECT COUNT(*) FROM NhapDK) > COUNT(*)) FROM DK;
SELECT 'avg_s1=' || printf('%.1f', AVG(diem)) FROM DK WHERE mssv='S1';
