-- Lab tuỳ chọn trên Oracle thật (bnx-ora) cho BNX L06: giao dịch chuyển tiền & hoàn tác khi vi phạm CHECK
WHENEVER SQLERROR CONTINUE
SET SERVEROUTPUT ON
BEGIN EXECUTE IMMEDIATE 'DROP TABLE bnx_l06_lab_tk'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
CREATE TABLE bnx_l06_lab_tk (id NUMBER PRIMARY KEY, so_du NUMBER CHECK (so_du >= 0));
INSERT INTO bnx_l06_lab_tk VALUES (1, 500000);
INSERT INTO bnx_l06_lab_tk VALUES (2, 400000);
INSERT INTO bnx_l06_lab_tk VALUES (3, 400000);
COMMIT;

CREATE OR REPLACE PROCEDURE bnx_l06_lab_chuyen(p_a NUMBER, p_b NUMBER, p_tien NUMBER) IS
BEGIN
  SAVEPOINT sp_start;
  UPDATE bnx_l06_lab_tk SET so_du = so_du + p_tien WHERE id = p_b;
  UPDATE bnx_l06_lab_tk SET so_du = so_du - p_tien WHERE id = p_a;
  COMMIT;
  DBMS_OUTPUT.PUT_LINE('chuyen ' || p_a || '->' || p_b || ' ' || p_tien || ': OK');
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK TO sp_start;
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('chuyen ' || p_a || '->' || p_b || ' ' || p_tien || ': loi so du khong du');
END;
/
BEGIN
  bnx_l06_lab_chuyen(1, 2, 200000);
  bnx_l06_lab_chuyen(2, 3, 900000);
END;
/
SELECT 'tong_tien=' || SUM(so_du) AS kq FROM bnx_l06_lab_tk;
