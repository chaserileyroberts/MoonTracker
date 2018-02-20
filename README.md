# MoonTracker
Moon tracker SD&amp;D Project

[![Build Status](https://travis-ci.org/Thenerdstation/MoonTracker.svg?branch=master)](https://travis-ci.org/Thenerdstation/MoonTracker)

## Building

To get the source, you can either git clone or just download the zip file and extract it somewhere.

```bash
git clone https://github.com/Thenerdstation/MoonTracker.git
cd MoonTracker
```
### Installing Dependencies

First you'll need Python 3, pip, and SQLite, if you don't have them already.

```bash
sudo apt install python3
sudo apt install python3-pip
sudo apt install libsqlite3-dev
```
### Setting up the Virtual Environment

It's recommended you build the application from a virtual environment, to ensure the Python packages used for the project are isolated from the rest of the system, to avoid version conflicts. You can skip this step if you're fine with overwriting the versions of any packages you already have that the application uses.

```bash 
sudo apt install python3-venv
python3 -m venv .
```
To automatically use the virtual environment every time you cd into the directory, use autoenv.

```
sudo pip3 install setuptools
sudo pip3 install autoenv
echo "source `which activate.sh`" >> ~/.bashrc
source ~/.bashrc
```

Now, whenever you cd into MoonTracker, you'll automatically enter the virtual environment. Use `deactivate` to leave it. cd out and back into the directory now to make sure it works.

```
cd ..
cd MoonTracker
```

### Installing Python Packages

You can automatically install all of the Python packages used by the project with pip and the requirements.txt.

`pip install -r requirements.txt`

### Adding api_keys.py to the Project

Next, add api_keys.py to the root directory of the project.

### Running

Run using the following command.

`python app.py`
