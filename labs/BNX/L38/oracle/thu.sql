-- Lab tuỳ chọn trên Oracle thật (bnx-ora) cho BNX L38: Oracle DBMS_AQ giao dịch thật
WHENEVER SQLERROR CONTINUE
SET SERVEROUTPUT ON
BEGIN DBMS_AQADM.STOP_QUEUE('bnx_l38_lab_q'); EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN DBMS_AQADM.DROP_QUEUE('bnx_l38_lab_q'); EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN DBMS_AQADM.DROP_QUEUE_TABLE('bnx_l38_lab_qt', TRUE); EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TYPE bnx_l38_lab_msg'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
WHENEVER SQLERROR EXIT FAILURE
CREATE TYPE bnx_l38_lab_msg AS OBJECT (ma_gd NUMBER, so_tien NUMBER);
/
BEGIN
  DBMS_AQADM.CREATE_QUEUE_TABLE(queue_table => 'bnx_l38_lab_qt', queue_payload_type => 'bnx_l38_lab_msg');
  DBMS_AQADM.CREATE_QUEUE(queue_name => 'bnx_l38_lab_q', queue_table => 'bnx_l38_lab_qt');
  DBMS_AQADM.START_QUEUE(queue_name => 'bnx_l38_lab_q');
END;
/
DECLARE
  eo DBMS_AQ.ENQUEUE_OPTIONS_T;
  mp DBMS_AQ.MESSAGE_PROPERTIES_T;
  mh RAW(16);
  msg bnx_l38_lab_msg;
  dq DBMS_AQ.DEQUEUE_OPTIONS_T;
  cnt NUMBER;
BEGIN
  DBMS_AQ.ENQUEUE('bnx_l38_lab_q', eo, mp, bnx_l38_lab_msg(201, 750000), mh);
  COMMIT;
  DBMS_AQ.ENQUEUE('bnx_l38_lab_q', eo, mp, bnx_l38_lab_msg(202, 300000), mh);
  ROLLBACK;
  DBMS_AQ.ENQUEUE('bnx_l38_lab_q', eo, mp, bnx_l38_lab_msg(203, 120000), mh);
  COMMIT;
  SELECT COUNT(*) INTO cnt FROM bnx_l38_lab_qt;
  DBMS_OUTPUT.PUT_LINE('sau_gui=' || cnt);
  dq.wait := DBMS_AQ.NO_WAIT;
  DBMS_AQ.DEQUEUE('bnx_l38_lab_q', dq, mp, msg, mh);
  COMMIT;
  DBMS_OUTPUT.PUT_LINE('nhan=' || msg.ma_gd || ' ' || msg.so_tien);
  SELECT COUNT(*) INTO cnt FROM bnx_l38_lab_qt;
  DBMS_OUTPUT.PUT_LINE('con_lai=' || cnt);
END;
/
