# Coderun-backend

## How to setup?

The first thing to do is to clone the repository:

```sh
$ https://github.com/kabirdutt0907/o1analysis.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv venv
$ venv\Scripts\activate
```

Then install the dependencies:

```sh
(venv)$ cd apti_backend
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:
```sh
(venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.
