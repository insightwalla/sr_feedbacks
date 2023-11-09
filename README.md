
### SETUP

```bash
# macos
virtualenv venv -p python3
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

```bash
# windows
python -m venv venv
venv/Scripts/activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Script
```bash
streamlit run main_1.py
```

## DESCRIPTION
---

The goal of this project is to connect to the 7rooms API and query their database of Feedbacks.
