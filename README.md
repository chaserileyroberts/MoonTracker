# MoonTracker

Moon tracker SD&amp;D Project

[![Build Status](https://travis-ci.org/Thenerdstation/MoonTracker.svg?branch=master)](https://travis-ci.org/Thenerdstation/MoonTracker)

[![Test Coverage](https://api.codeclimate.com/v1/badges/1ed309ba3e7b7d6c7329/test_coverage)](https://codeclimate.com/github/Thenerdstation/MoonTracker/test_coverage)

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

### Setting up the Virtual Environment (Optional)

It's recommended you build the application from a virtual environment, to ensure the Python packages used for the project are isolated from the rest of the system, to avoid version conflicts. You can skip this step if you're fine with overwriting the versions of any packages you already have that the application uses.

To prevent the virtual environment from interfering with the project, it's recommended you store the virtual environment somewhere outside of the project root directory, such as ~/envs/MoonTracker-env

```bash 
sudo apt install python3-venv
python3 -m venv ~/envs/MoonTracker-env
```

Then, whenever you want to work on the project, source to wherever you're virtual environment is.

```bash
source ~/envs/MoonTracker-env/bin/activate
```

### Installing Python Packages

You can automatically install all of the Python packages used by the project with pip and the requirements.txt.

```bash
pip install -r requirements.txt
```

### Adding api_keys.py to the Project

The application requires API keys for Twilio and Recaptcha. Create an api_keys.py file under the moontracker folder, and add the API keys formatted as follows.

```text
twilio_sid = <twilio_sid>
twilio_auth = <twilio_auth>
recaptcha_public = <recaptcha_public>
recaptcha_private = <recaptcha_private>
```

### Running

Run using the following command.

```bash
python start.py
```
