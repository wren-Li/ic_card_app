from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')

# 初始化数据库
def init_db():
    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    # 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        card_uid TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        phone TEXT NOT NULL,
        user_type TEXT NOT NULL DEFAULT 'parent',
        parent_uid TEXT,
        points INTEGER DEFAULT 0,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (parent_uid) REFERENCES users (card_uid)
    )
    ''')
    # 积分记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS points_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_uid TEXT NOT NULL,
        change_points INTEGER NOT NULL,
        current_points INTEGER NOT NULL,
        operation_type TEXT NOT NULL,
        operator_uid TEXT NOT NULL,
        operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (card_uid) REFERENCES users (card_uid)
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 1. 开户接口
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    card_uid = data.get('card_uid')
    username = data.get('username')
    phone = data.get('phone')
    user_type = data.get('user_type', 'parent')
    parent_uid = data.get('parent_uid', '')

    if not all([card_uid, username, phone, user_type]):
        return jsonify({'code': 400, 'msg': '参数不全'}), 400
    if user_type not in ['parent', 'child']:
        return jsonify({'code': 400, 'msg': '用户类型只能是parent/child'}), 400
    if user_type == 'child' and not parent_uid:
        return jsonify({'code': 400, 'msg': '子女账户必须绑定家长UID'}), 400

    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE card_uid = ?', (card_uid,))
        if cursor.fetchone():
            return jsonify({'code': 409, 'msg': '该IC卡已开户'}), 200
        if user_type == 'child':
            cursor.execute('SELECT user_type FROM users WHERE card_uid = ?', (parent_uid,))
            res = cursor.fetchone()
            if not res or res[0] != 'parent':
                return jsonify({'code': 404, 'msg': '绑定的家长不存在'}), 200
        cursor.execute(
            'INSERT INTO users (card_uid, username, phone, user_type, parent_uid) VALUES (?, ?, ?, ?, ?)',
            (card_uid, username, phone, user_type, parent_uid if user_type == 'child' else None)
        )
        conn.commit()
        return jsonify({'code': 200, 'msg': '开户成功'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'code': 500, 'msg': f'开户失败：{str(e)}'}), 500
    finally:
        conn.close()

# 2. 积分查询接口
@app.route('/api/query', methods=['POST'])
def query_points():
    data = request.get_json()
    card_uid = data.get('card_uid')
    if not card_uid:
        return jsonify({'code': 400, 'msg': '请传入IC卡UID'}), 400
    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, phone, points, user_type, parent_uid FROM users WHERE card_uid = ?', (card_uid,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'code': 404, 'msg': '该IC卡未开户'}), 200
    # 查询积分记录
    cursor.execute('''
    SELECT change_points, current_points, operation_type, operation_time, operator_uid 
    FROM points_records WHERE card_uid = ? ORDER BY operation_time DESC LIMIT 10
    ''', (card_uid,))
    records = cursor.fetchall()
    record_list = []
    for r in records:
        cursor.execute('SELECT username FROM users WHERE card_uid = ?', (r[4],))
        operator = cursor.fetchone()
        record_list.append({
            'change_points': r[0], 'current_points': r[1], 'operation_type': r[2],
            'operation_time': r[3], 'operator_name': operator[0] if operator else '未知'
        })
    conn.close()
    return jsonify({
        'code': 200, 'msg': '查询成功',
        'data': {
            'username': user[0], 'phone': user[1], 'points': user[2],
            'user_type': user[3], 'parent_uid': user[4], 'records': record_list
        }
    }), 200

# 3. 积分增减接口
@app.route('/api/update_points', methods=['POST'])
def update_points():
    data = request.get_json()
    operator_uid = data.get('operator_uid')
    target_uid = data.get('target_uid')
    change_points = data.get('change_points')
    operation_type = data.get('operation_type', '消费')
    if not all([operator_uid, target_uid, change_points]):
        return jsonify({'code': 400, 'msg': '参数不全'}), 400
    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    conn.execute('BEGIN TRANSACTION')
    try:
        # 校验操作人是家长
        cursor.execute('SELECT user_type FROM users WHERE card_uid = ?', (operator_uid,))
        res = cursor.fetchone()
        if not res or res[0] != 'parent':
            return jsonify({'code': 403, 'msg': '仅家长可操作'}), 200
        # 校验目标用户
        cursor.execute('SELECT parent_uid, points FROM users WHERE card_uid = ?', (target_uid,))
        target = cursor.fetchone()
        if not target:
            return jsonify({'code': 404, 'msg': '被操作人未开户'}), 200
        # 校验操作权限（自己或绑定的子女）
        if target_uid != operator_uid and target[0] != operator_uid:
            return jsonify({'code': 403, 'msg': '仅可操作自己或绑定的子女'}), 200
        # 计算新积分
        new_points = target[1] + int(change_points)
        if new_points < 0:
            return jsonify({'code': 403, 'msg': '积分不足'}), 200
        # 更新积分
        cursor.execute('UPDATE users SET points = ? WHERE card_uid = ?', (new_points, target_uid))
        # 记录积分变动
        cursor.execute('''
        INSERT INTO points_records (card_uid, change_points, current_points, operation_type, operator_uid)
        VALUES (?, ?, ?, ?, ?)
        ''', (target_uid, change_points, new_points, operation_type, operator_uid))
        conn.commit()
        return jsonify({'code': 200, 'msg': '操作成功', 'data': {'current_points': new_points}}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'code': 500, 'msg': f'操作失败：{str(e)}'}), 500
    finally:
        conn.close()

# 4. 查询绑定子女
@app.route('/api/query_children', methods=['POST'])
def query_children():
    data = request.get_json()
    parent_uid = data.get('parent_uid')
    if not parent_uid:
        return jsonify({'code': 400, 'msg': '请传入家长UID'}), 400
    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    cursor.execute('SELECT card_uid, username, phone, points FROM users WHERE parent_uid = ?', (parent_uid,))
    children = cursor.fetchall()
    conn.close()
    return jsonify({
        'code': 200, 'msg': '查询成功',
        'data': [{'card_uid': c[0], 'username': c[1], 'phone': c[2], 'points': c[3]} for c in children]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)