@echo off
echo [Create virtual environment]
python -m venv env
echo Done...

echo [Activate virtual environment]
call env\Scripts\activate.bat
echo Done...

echo [Update pip]
python -m pip install --upgrade pip
echo Done...

echo [Install requirements]
pip install -r requirements.txt
echo Done...

