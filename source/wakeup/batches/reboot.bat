@echo off
rem reboot.bat [pid]
rem kill process
taskkill /pid %1 -f

rem check web connection
echo "begin ping www.baidu.com"

set ping_time=0
:loop
echo %date% : %time%
ping www.baidu.com
set return_value=%ERRORLEVEL%
set /A ping_time=ping_time+1
IF NOT %return_value%==0 (
    timeout 4
    echo "ping times : %ping_time%"
    goto loop
)



rem reboot now 
start cmd /c python %2/main.py