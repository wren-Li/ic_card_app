@echo off
chcp 65001 >nul
echo ====================
echo IC卡积分系统启动中...
echo ====================
echo "第一步：检查Python环境"
python --version >nul 2>&1
if errorlevel 1 (
    echo "错误：没装Python！先装Python并添加到环境变量"
    pause
    exit
)
echo "Python环境正常！"
echo "第二步：安装依赖"
pip install flask flask-cors >nul 2>&1
echo "依赖安装完成！"
echo "第三步：启动后端服务"
echo "外网访问地址：http://116aj32013lz6.vicp.fun:37660"
echo "不要关闭这个窗口！"
python app.py
pause