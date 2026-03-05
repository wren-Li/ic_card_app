import sqlite3
import uuid

# 连接数据库
conn = sqlite3.connect('ic_card_points.db')
cursor = conn.cursor()

# 创建家长测试账户
parent_account_id = 'TEST_PARENT'
parent_password = '123456'
parent_card_uid = 'TEST_PARENT_UID'

# 检查家长账户是否已存在
cursor.execute('SELECT account_id FROM users WHERE account_id = ?', (parent_account_id,))
if not cursor.fetchone():
    # 插入家长账户
    cursor.execute(
        'INSERT INTO users (card_uid, account_id, password, user_type, parent_uid, points) VALUES (?, ?, ?, ?, ?, ?)',
        (parent_card_uid, parent_account_id, parent_password, 'parent', None, 0)
    )
    print(f"家长测试账户创建成功: 账户ID={parent_account_id}, 密码={parent_password}")
else:
    print(f"家长测试账户已存在: 账户ID={parent_account_id}")

# 创建子女测试账户
child_account_id = 'TEST_CHILD'
child_password = '123456'
child_card_uid = 'TEST_CHILD_UID'

# 检查子女账户是否已存在
cursor.execute('SELECT account_id FROM users WHERE account_id = ?', (child_account_id,))
if not cursor.fetchone():
    # 插入子女账户，绑定到刚创建的家长账户
    cursor.execute(
        'INSERT INTO users (card_uid, account_id, password, user_type, parent_uid, points) VALUES (?, ?, ?, ?, ?, ?)',
        (child_card_uid, child_account_id, child_password, 'child', parent_card_uid, 0)
    )
    # 创建初始积分记录
    cursor.execute(
        'INSERT INTO points_records (card_uid, change_points, current_points, operation_type, operator_uid) VALUES (?, ?, ?, ?, ?)',
        (child_card_uid, 0, 0, '账户开户', 'system')
    )
    print(f"子女测试账户创建成功: 账户ID={child_account_id}, 密码={child_password}, 绑定家长UID={parent_card_uid}")
else:
    print(f"子女测试账户已存在: 账户ID={child_account_id}")

# 提交事务并关闭连接
conn.commit()
conn.close()

print("\n测试账户信息:")
print("家长账户:")
print(f"  账户ID: {parent_account_id}")
print(f"  密码: {parent_password}")
print(f"  UID: {parent_card_uid}")
print("子女账户:")
print(f"  账户ID: {child_account_id}")
print(f"  密码: {child_password}")
print(f"  UID: {child_card_uid}")
