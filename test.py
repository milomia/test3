#/usr/bin/python
# more tests

import sqlite3

conn = sqlite3.connect('suade.db')
print("Opened database successfully");

conn=sqlite3.connect('suade.db')
sqlStr="select sum(quantity) from orders inner join orderline on orders.order_id = orderline.order_id and created_at BETWEEN '2019-09-01' and '2019-09-02'"
breakpoint()
cursor=conn.execute(sqlStr)
for row in cursor:
  print(row[0])

print("Operation done successfully");
conn.close()
