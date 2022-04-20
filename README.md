**This is a simple films browser website built with Django.**

![superfilms](https://user-images.githubusercontent.com/64534303/164229221-01c653d8-d3fb-43cb-8cb9-84eae3eb5556.png)


Search movies by a single category or multiple criterias. Used DRF for API.

## Quickstart
Create a virtual environment to store your projects dependencies separately.

` pip install virtualenv `

` virtual venv `

This will create a new directory called ` venv `.

Clone or download this repository.

` git clone https://github.com/lukitoziomal/superfilms.git `

Activate your virtual environment.

` path-to-venv\venv\Scripts\activate `

Install project dependencies.

` pip install -r requirements.txt `

Setup the database. Change ` DATABASES ` properties in ` movies\settings.py ` if needed. Then run:

` python manage.py migrate `


Add movies to database. Use ` movies10.csv ` for sample of few movies or ` movies.csv ` to get over 25k records - this will take a while to load.

` python manage.py runscript addmovies `

Run server.

` python manage.py runserver `


Bootstrap template and .css files taken from https://startbootstrap.com for non-commercial use.
