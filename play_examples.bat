@echo off
set PYTHONPATH=%PYTHONPATH%;%~dp0
set PATH=%PATH%;%~dp0\lib
cd ./examples/
python example_player.py
pause