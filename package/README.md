# <bootstrap-title>

<bootstrap-description>.

## For Consumers

### Installation

```bash
python3.<bootstrap-python-minor> -m venv .venv
source .venv/bin/activate
```

## For Developers

### Cloning the project

Execute the following commands:
```bash
git clone <bootstrap-repo-git>
cd <bootstrap-dir>
```

### Prepare a virtual environment

Execute the following commands:
```bash
python3.<bootstrap-python-minor> -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Prepare repository hooks

Execute the following commands:
```bash
pre-commit autoupdate
pre-commit install
```
