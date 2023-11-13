<!-- ABOUT THE PROJECT -->
## About The Project

This is the backend for the VandyPool web application. This app was deployed with Heroku. Here is the link to the front-end project: https://github.com/jzjackjz/VandyPool/


### Built With

Our full-stack project was bulit with the following languages and frameworks:

* React
* Python
* Django Framework
* Heroku + Vercel

### Getting Started

1. First clone the git repository
2. Run ```cp .env.example .env``` to copy the example.env files to .env files. Replace the empty placeholders with the appropriate values.
3. Make sure Docker is installed. To spin up Docker, run ```docker-compose up --build```.
4. Migrate the database while Docker is spun up: ```docker-compose exec web python manage.py migrate```
