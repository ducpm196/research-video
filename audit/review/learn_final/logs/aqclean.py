import sys
sys.path.insert(0, "audit/bnx")
import dbrun
sql = """BEGIN
  DBMS_AQADM.DROP_QUEUE_TABLE(queue_table => 'bnx_l07_qt', force => TRUE);
END;
/
SELECT COUNT(*) AS con_lai FROM user_queue_tables;
SELECT COUNT(*) AS bang_qt FROM user_objects WHERE object_name = 'BNX_L07_QT';"""
print(dbrun.ora(sql))
