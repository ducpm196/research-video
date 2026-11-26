-- Lab tuỳ chọn trên Oracle thật (bnx-ora: gvenzl/oracle-free:23-slim) cho BNK L05
-- Kiểm khoá hàng SELECT ... FOR UPDATE theo thứ tự id tăng dần và tổng tiền bảo toàn
WHENEVER SQLERROR EXIT FAILURE
SET SERVEROUTPUT ON
BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE bnk_l05_lab_tk';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
CREATE TABLE bnk_l05_lab_tk (id NUMBER PRIMARY KEY, so_du NUMBER NOT NULL);
INSERT INTO bnk_l05_lab_tk VALUES (4, 1000);
INSERT INTO bnk_l05_lab_tk VALUES (7, 1000);
INSERT INTO bnk_l05_lab_tk VALUES (9, 1000);
COMMIT;

CREATE OR REPLACE PROCEDURE bnk_l05_lab_khoa(p_from NUMBER, p_to NUMBER) IS
  v_first NUMBER := LEAST(p_from, p_to);
  v_second NUMBER := GREATEST(p_from, p_to);
  v_b1 NUMBER;
  v_b2 NUMBER;
BEGIN
  SELECT so_du INTO v_b1 FROM bnk_l05_lab_tk WHERE id = v_first FOR UPDATE;
  SELECT so_du INTO v_b2 FROM bnk_l05_lab_tk WHERE id = v_second FOR UPDATE;
  DBMS_OUTPUT.PUT_LINE(p_from || '->' || p_to || ': khoa ' || v_first || ' roi ' || v_second);
  COMMIT;
END;
/
BEGIN
  bnk_l05_lab_khoa(4, 9);
  bnk_l05_lab_khoa(9, 4);
  bnk_l05_lab_khoa(7, 4);
  bnk_l05_lab_khoa(4, 7);
END;
/
SELECT 'tong_tien=' || SUM(so_du) AS kq FROM bnk_l05_lab_tk;
