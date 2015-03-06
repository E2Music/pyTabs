@echo off
set PYTHONPATH=%PYTHONPATH%;%~dp0
set PATH=%PATH%;%~dp0\lib
cd ./pytabs/gui/
start pythonw startApp.py
cd ../..