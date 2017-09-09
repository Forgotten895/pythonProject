@echo off

setlocal enabledelayedexpansion

set /a cha=1

(for /f "delims=" %%i in ('dir /b /s /a-d *.py') do (
	
    	echo !cha! : %%~ni
	set /a cha+=1
))

:no
set /p option=请输入你的选择:
set /a cha=1

(for /f "delims=" %%i in ('dir /b /s /a-d *.py') do (
	if !cha! == !option! (
		set  dir=%%~ni)
	set /a cha+=1))

echo 你选择的文件为：!dir!.py

set /p KEY=输入N回车重新选择文件，按其它键则开始转换，回车确定 ：

(if !KEY! == N (goto no)else (
echo ================================================
echo 启动转换
pause))
echo ================================================
echo 开始转换：
echo ================================================
cd /d "e:\c# program"
pyinstaller -F !dir!.py --onefile
echo ================================================
echo 转换结束。
echo ================================================

pause 

