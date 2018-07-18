FROM python:3.6.6-slim 

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

ENV NAME World

EXPOSE 5000

CMD ["python", "app.py"]