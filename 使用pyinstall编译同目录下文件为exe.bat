@echo off

setlocal enabledelayedexpansion

echo ================================================
echo 当前目录下可以转换的文件名：
echo 

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
set  KEY=0
set /p KEY=输入N回车重新选择文件，输入X隐藏黑窗，按其它键则开始转换，回车确定 ：


(if !KEY! == N (
	echo ================================================
	goto no))

(if !KEY! == n (
	echo ================================================
	goto no))

(if !KEY! == x (
	echo ================================================
	echo 隐藏黑窗模式已开启
	goto set))
(if !KEY! == X (
	echo ================================================
	echo 隐藏黑窗模式已开启
	goto set))
goto ok

:set
pause
echo ================================================
echo 开始转换：
echo ================================================
cd /d "e:\c# program"
pyinstaller -F  !dir!.py --noconsole
echo ================================================
echo 转换结束。
echo ================================================
goto end


:ok
pause
echo ================================================
echo 开始转换：
echo ================================================
cd /d "e:\c# program"
pyinstaller -F !dir!.py 
echo ================================================
echo 转换结束。
echo ================================================
goto end

:end
pause 
start %~dp0\dist 
