-- Lab tuỳ chọn trên Oracle thật (bnx-ora) cho BNX L37: chống SQL injection bằng bind variable
WHENEVER SQLERROR EXIT FAILURE
SET SERVEROUTPUT ON
BEGIN EXECUTE IMMEDIATE 'DROP TABLE bnx_l37_lab_tk'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
CREATE TABLE bnx_l37_lab_tk (ten VARCHAR2(50), so_du NUMBER);
INSERT INTO bnx_l37_lab_tk VALUES ('An', 500);
INSERT INTO bnx_l37_lab_tk VALUES ('Binh', 700);
INSERT INTO bnx_l37_lab_tk VALUES ('Chi', 900);
INSERT INTO bnx_l37_lab_tk VALUES ('Dung', 100);
COMMIT;

DECLARE
  v_ghep NUMBER;
  v_bind NUMBER;
  procedure kiem(p_idx NUMBER, p_in VARCHAR2) IS
  BEGIN
    EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM bnx_l37_lab_tk WHERE ten = ''' || p_in || '''' INTO v_ghep;
    EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM bnx_l37_lab_tk WHERE ten = :1' INTO v_bind USING p_in;
    DBMS_OUTPUT.PUT_LINE('chuoi ' || p_idx || ': ghep ' || v_ghep || ' dong, bind ' || v_bind || ' dong');
  END;
BEGIN
  kiem(1, 'An');
  kiem(2, 'X'' OR ''1''=''1');
END;
/
