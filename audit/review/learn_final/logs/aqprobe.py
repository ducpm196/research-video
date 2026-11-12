import sys
sys.path.insert(0, "audit/bnx")
import dbrun
q = """SELECT queue_table, name, queue_type FROM user_queues
UNION ALL SELECT queue_table, 'QT', 'x' FROM user_queue_tables
UNION ALL SELECT object_name, object_type, status FROM user_objects WHERE object_name LIKE 'BNX_L07%' AND object_type IN ('TYPE','QUEUE','TABLE');"""
print(dbrun.ora(q))
