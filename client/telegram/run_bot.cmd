@echo off
echo [Activate virtual environment]
call env\Scripts\activate.bat
echo Done...

echo [Run bot.py]
start "SmartHeartBot" cmd /K @python.exe bot.py