@echo off

setlocal enabledelayedexpansion

echo ================================================
echo ��ǰĿ¼�¿���ת�����ļ�����
echo 

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
set  KEY=0
set /p KEY=����N�س�����ѡ���ļ�������X���غڴ�������������ʼת�����س�ȷ�� ��


(if !KEY! == N (
	echo ================================================
	goto no))

(if !KEY! == n (
	echo ================================================
	goto no))

(if !KEY! == x (
	echo ================================================
	echo ���غڴ�ģʽ�ѿ���
	goto set))
(if !KEY! == X (
	echo ================================================
	echo ���غڴ�ģʽ�ѿ���
	goto set))
goto ok

:set
pause
echo ================================================
echo ��ʼת����
echo ================================================
cd /d "e:\c# program"
pyinstaller -F  !dir!.py --noconsole
echo ================================================
echo ת��������
echo ================================================
goto end


:ok
pause
echo ================================================
echo ��ʼת����
echo ================================================
cd /d "e:\c# program"
pyinstaller -F !dir!.py 
echo ================================================
echo ת��������
echo ================================================
goto end

:end
pause 
start %~dp0\dist 
