@echo off

setlocal enabledelayedexpansion

set /a cha=1

(for /f "delims=" %%i in ('dir /b /s /a-d *.py') do (
	
    	echo !cha! : %%~ni
	set /a cha+=1
))

:no
set /p option=���������ѡ��:
set /a cha=1

(for /f "delims=" %%i in ('dir /b /s /a-d *.py') do (
	if !cha! == !option! (
		set  dir=%%~ni)
	set /a cha+=1))

echo ��ѡ����ļ�Ϊ��!dir!.py

set /p KEY=����N�س�����ѡ���ļ�������������ʼת�����س�ȷ�� ��

(if !KEY! == N (goto no)else (
echo ================================================
echo ����ת��
pause))
echo ================================================
echo ��ʼת����
echo ================================================
cd /d "e:\c# program"
pyinstaller -F !dir!.py --onefile
echo ================================================
echo ת��������
echo ================================================

pause 

