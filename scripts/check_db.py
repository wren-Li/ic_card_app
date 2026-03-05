import sqlite3

# 连接到数据库
conn = sqlite3.connect('ic_card_points.db')
cursor = conn.cursor()

# 检查users表结构
print('检查users表结构:')
cursor.execute('PRAGMA table_info(users)')
columns = cursor.fetchall()
for column in columns:
    print(f'列名: {column[1]}, 类型: {column[2]}, 是否为主键: {column[5]}')

# 检查points_records表结构
print('\n检查points_records表结构:')
cursor.execute('PRAGMA table_info(points_records)')
columns = cursor.fetchall()
for column in columns:
    print(f'列名: {column[1]}, 类型: {column[2]}, 是否为主键: {column[5]}')

# 关闭连接
conn.close()
