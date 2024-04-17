FROM python:3.10

ENV PYTHONPATH /usr/src/app

RUN mkdir -p $PYTHONPATH
RUN mkdir -p $PYTHONPATH/static

# where the code lives
WORKDIR $PYTHONPATH

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN chmod -R 755 /usr/src/app/static/

# install app and dependencies
COPY . $PYTHONPATH
RUN pip install --upgrade pip
COPY ./requirements.txt $PYTHONPATH
RUN pip install Django
RUN pip install -r requirements.txt

#Наполнение базы
CMD echo "yes" | python manage.py flush --no-input && \
python manage.py migrate && python seed/seed_script.py && \
python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --log-level info

