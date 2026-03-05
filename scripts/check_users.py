import sqlite3

# 连接到数据库
conn = sqlite3.connect('ic_card_points.db')
cursor = conn.cursor()

# 查询所有用户记录
print('查询所有用户记录:')
cursor.execute('SELECT card_uid, account_id, username, phone, user_type, points FROM users')
users = cursor.fetchall()

if users:
    for user in users:
        print(f'card_uid: {user[0]}, account_id: {user[1]}, username: {user[2]}, phone: {user[3]}, user_type: {user[4]}, points: {user[5]}')
else:
    print('没有用户记录')

# 关闭连接
conn.close()
