from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 数据库初始化
def init_db():
    conn = sqlite3.connect('ic_card_points.db')
    cursor = conn.cursor()
    # 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        card_uid TEXT PRIMARY KEY,
        account_id TEXT UNIQUE,
        password TEXT,
        user_type TEXT NOT NULL DEFAULT 'parent',
        parent_uid TEXT,
        points INTEGER DEFAULT 0
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
        operator_uid TEXT,
        operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    account_id = data.get('account_id')
    password = data.get('password')
    card_uid = data.get('card_uid')
    
    # 账户密码登录
    if account_id and password:
        conn = sqlite3.connect('ic_card_points.db')
        cursor = conn.cursor()
        cursor.execute('SELECT card_uid, account_id, password, user_type FROM users WHERE account_id = ? AND password = ?', (account_id, password))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return jsonify({'code': 401, 'msg': '账户或密码错误'}), 200
        return jsonify({
            'code': 200, 'msg': '登录成功',
            'data': {
                'card_uid': user[0], 'account_id': user[1], 'password': user[2],
                'user_type': user[3]
            }
        }), 200
    # IC卡登录
    elif card_uid:
        conn = sqlite3.connect('ic_card_points.db')
        cursor = conn.cursor()
        cursor.execute('SELECT card_uid, account_id, password, user_type FROM users WHERE card_uid = ?', (card_uid,))
        user = cursor.fetchone()
        conn.close()
        if not user:
            return jsonify({'code': 401, 'msg': 'IC卡未开户'}), 200
        return jsonify({
            'code': 200, 'msg': '登录成功',
            'data': {
                'card_uid': user[0], 'account_id': user[1], 'password': user[2],
                'user_type': user[3]
            }
        }), 200
    else:
        return jsonify({'code': 400, 'msg': '参数不全'}), 400

# 根路径
@app.route('/', methods=['GET'])
def index():
    return jsonify({"code": 200, "msg": "后端服务正常运行", "data": None})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
