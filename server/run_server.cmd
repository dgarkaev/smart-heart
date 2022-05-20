@echo off
echo [Activate virtual environment]
call env\Scripts\activate.bat
echo Done...

echo [Run worker.py]
start "SmartHeartWorker" cmd /K @python.exe worker.py