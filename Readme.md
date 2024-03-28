Install Python On Local System

create virtual env
install requirements file

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

For Docker

sudo docker build -t image_name
sudo docker run --name <name> -p 8000:8000 image_name
docker-compose up -d