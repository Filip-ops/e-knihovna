# e-knihovna

## Install dependencies + setup

- Windows:
  - Git, Python 3 + pip3, [PostrgreSQL](https://www.postgresql.org/download/), [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Linux (Debian/Ubuntu/PopOS):
  - ```sudo apt install -y git python3 python3-pip postresql libpq-dev snap```
  - ```sudo snap install --classic heroku```
  
- ```heroku login```
- Clone the repository, ```cd e-knihovna```
- Run the setup:
  - Windows:
  ```heroku local setup -f Procfile.windows``` or ```pip install --user -r requirements.txt```
  - UNIX-like:
  ```heroku local setup``` or ```pip3 install -r requirements.txt```

## Start the project locally

- First step when not already ran: ```heroku local collectstatic```
- Run the server:
  - Windows:
  ```heroku local web -f Procfile.windows``` or ```python manage.py runserver 0:5000```
  - UNIX-like:
  ```heroku local web``` or ```python3 manage.py runserver 0:5000```
- Open browser at: ```localhost:5000```

## Pushing changes to the repository

Use **VS Code** Git GUI (RECOMMENDED), etc. or manually:

- ```git add .```
- ```git commit -m "Message"```
- ```git push```

## Web deployment

Site is automatically deployed when pushed to Github repository if everything is OK.

**Test the site before pushing to Github!**

## Databases

Both local project and deployed web is running on the same online database. Every migration, even local, will make changes to the DB.

When made changes to ```models.py``` files, you have to run:

- ```$ heroku run python``` 
- ```>>>from flasklib import db```
- ```>>>db.create_all()```
- ```>>>exit()```

which will update (create/delete/...) corresponding DB tables.
