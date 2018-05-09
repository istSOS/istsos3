# Developing

## Setting up development environment

Start by [forking](https://github.com/istSOS/istsos3/fork) the istSOS3 repository.

## Preparing for publication

### Requirements

```bash
sudo apt-get install python3-venv
sudo pip3 install -U setuptools
```

### Create distribution package 

```bash
python3 setup.py sdist
```

### Upload to pypi

```bash
twine upload dist/*
```

### Test

```bash
python3 -m venv tutorial
source tutorial/bin/activate
pip install --upgrade pip
pip install dist/istsos-3.0.0b1.tar.gz
```

Exit from venv

```bash
deactivate
```

