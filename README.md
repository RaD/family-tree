# Homesite Django Project #
## Prerequisites ##

- python >= 2.7
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python enviroment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv env
```

#### For virtualenv ####
```bash
virtualenv env
cd env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone https://github.com/RaD/family-tree.git ft
```

### Install requirements ###
```bash
cd ft
pip install -r reqs/base.txt
```

### Sync database ###
```bash
python manage.py syncdb --migrate
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000/galleria/
