import sqlite3

# 连接数据库
conn = sqlite3.connect('ic_card_points.db')
cursor = conn.cursor()

# 查询用户密码
cursor.execute('SELECT account_id, password, user_type FROM users WHERE account_id IN (?, ?)', ('TEST_PARENT', 'TEST_CHILD'))
users = cursor.fetchall()

print("用户密码信息:")
for user in users:
    account_id, password, user_type = user
    print(f"账户ID: {account_id}, 密码: '{password}', 类型: {user_type}")

# 关闭连接
conn.close()
