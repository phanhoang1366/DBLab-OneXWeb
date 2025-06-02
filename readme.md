# Light Novel Database for Python
This is a code jam, a small project to create a light novel database in Python. The goal is to create a simple database that can be used to store information about light novels, such as title, author, publisher, and other relevant information.

## Installation
First, install MariaDB or MySQL, and then install the Python dependencies. You can do this by running the following command:

```bash
sudo apt install mariadb-server python-is-python3 python3-pip python3-venv libmariadb-dev # libmysqlclient-dev; assuming you are on a Debian-based system
```

Make a virtual environment, install the requirements in `requirements.txt`, make changes to the `config.py` and .env file just like every other Django project, and run the migrations.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py createsuperuser
```

Also we have `local_settings.py` which is used to override the settings in `settings.py`. You can use this file to set your own settings, such as the database type and other settings. Look at the `local_settings.py.example` file for an example of how to use it.

Follow the DigitalOcean tutorial on how to set up a Django project with MariaDB or MySQL for production:
https://www.digitalocean.com/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu#step-6-testing-gunicorn-s-ability-to-serve-the-project

## Limitations
This is a code jam, so there are some limitations. The database is not fully normalized, and there are some hardcoded values in the code. The goal is to create a simple database that can be used to store information about light novels, not a fully-fledged database.

Also, the images uploaded to the database are not compressed, so they may take up a lot of space. There are no plans to compress the images, but you can use a tool like Pillow to compress the images before uploading them to the database.