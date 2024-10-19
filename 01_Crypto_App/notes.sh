# Check version of python
python --version
# if 3.10 version of windows not installed
# Create venv with python 3.10
py -3.10 -m venv venv
# Run venv
. venv/Scripts/activate
# Run release of pip:
python.exe -m pip install --upgrade pip
# Install from requirements.txt
pip install -r requirements.txt
# If problem with long path open power shell:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
# Run program:
streamlit run main.py

