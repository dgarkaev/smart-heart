@echo off
echo [Create virtual environment]
python -m venv env --clear --upgrade-deps
echo Done...

echo [Activate virtual environment]
call env\Scripts\activate.bat
echo Done...

echo [Install requirements]
pip install -r requirements.txt
echo Done...

