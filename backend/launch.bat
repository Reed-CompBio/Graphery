@echo off
py -3 --version
if errorlevel 1 goto errorNoPython

:execLocalServer
py -3 "%~dp0user_server.py"
pause
exit

:errorNoPython
echo.
echo Error^: Python not installed
pause
exit

