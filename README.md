# 🌟 Welcome to the ThoughtFull Engineering Challenge: MindWellnessChat Edition!

## Setup & Installation

### Install Database
- CREATE DATABASE healthchat;
- CREATE USER healthchat_user WITH PASSWORD 'healthchat_pass';
- ALTER ROLE healthchat_user SET client_encoding TO 'utf8';
- ALTER ROLE healthchat_user SET default_transaction_isolation TO 'read committed';
- ALTER ROLE healthchat_user SET timezone TO 'UTC';
- GRANT ALL PRIVILEGES ON DATABASE healthchat TO healthchat_user;

### Make Pyhton environment & install dependencies  (Python3.10+ required)
- python3 -m venv healthchat_env
- source healthchat_env/bin/activate
- clone the project and switch to the PR's branch
- create `.env` file and copy `env_dev` content into it.
- pip install -r requirements.txt
- Run these commands to setup db migrations
    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py runserver


### How it Works?
#### Auth:
- Signup - Go to this path: /users/auth/register/
- Login - Go to this path: /users/auth/login/

#### after  login, you will go to this page (http://127.0.0.1:8000/) redirected to your dashboard page where you can start chatting with other users.

- you will see users list (you should signup with many account 2 or 3 to try it)
- Click on any user you want to chat with you will be redirected to the page to chat with it.
