@echo off
rem reboot.bat [pid]
rem kill process
taskkill /pid %1 -f
rem reboot now 
start cmd /c python %2/main.py