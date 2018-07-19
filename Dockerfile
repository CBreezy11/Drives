FROM python:3.6.6-slim 

WORKDIR /app

COPY app.py /app

RUN pip install Flask requests beautifulsoup4

ENV NAME World

EXPOSE 5000

CMD ["python", "app.py"]