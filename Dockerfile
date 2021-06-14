FROM python:3.8

RUN apt update
RUN apt upgrade -y
RUN apt install awscli cron -y



WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi:application"]
