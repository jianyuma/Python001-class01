import numpy as np
import pandas as pd

data1=pd.DataFrame({
    "id": range(15),
    "order_id":np.random.randint(1000,1050,15),
    "age":np.random.randint(15,50,15)
    })

data2=pd.DataFrame({
    "id": range(15),
    "salary":np.random.randint(1000,1050,15),
    "age":np.random.randint(15,50,15)
    })

#1. SELECT * FROM data;
data1
 	
#2. SELECT * FROM data LIMIT 10;
print(data1[0:10])
 	
#3. SELECT id FROM data;  //id 是 data 表的特定一列
print(data1['id'])
 
#4. SELECT COUNT(id) FROM data;
print(data1['id'].count())
 	
#5. SELECT * FROM data WHERE id<1000 AND age>30;
print(data1[(data1['id'] < 1000) & (data1['age'] > 30)])
 
#6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
data1.groupby('id').agg({'order_id': 'count'})
 	
#7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(data1 , data2 , on = 'id' how = 'inner')
 	
#8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([data1 , data2 ], axis = 1 ,join = 'inner')	
 	
#9. DELETE FROM table1 WHERE id=10;
data1.drop(data1[data1['id'] = 10])
 	
#10. ALTER TABLE table1 DROP COLUMN column_name;
data1.drop('age',axis = 1)