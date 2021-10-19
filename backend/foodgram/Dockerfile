FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r /code/requirements.txt
COPY . /code
CMD python /code/manage.py runserver 0:8000 