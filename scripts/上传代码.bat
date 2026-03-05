@echo off
chcp 65001
echo ====================
echo 上传代码到GitHub
echo ====================
set /p msg=输入本次改了啥（比如：修复读卡bug）：
git add .
git commit -m "%msg%"
git push
echo 上传成功！
pause