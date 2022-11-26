@echo off
python --version 2>NUL
if errorlevel 1 goto errorNoPython
pip --version 2>NUL
if errorlevel 1 goto errorNoPip

pip install pandas
pip install pillow
pip install quik
call python %~dp0Main.py

goto:eof

:errorNoPython
echo Error^: Python not installed and/or not in PATH environment variable. Add full path of your python.exe folder to PATH environment variable if you have installed Python
goto eof

:errorNoPip
echo Error^: Pip not installed and/or not in PATH environment variable. Add full path of your pip.exe folder to PATH environment variable if you have installed Pip
goto eof

:eof
pause
