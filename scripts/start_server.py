import subprocess
import sys

# 运行app.py并捕获输出
result = subprocess.run([sys.executable, 'app.py'], capture_output=True, text=True)
print('STDOUT:')
print(result.stdout)
print('\nSTDERR:')
print(result.stderr)
print('\nReturn code:', result.returncode)
