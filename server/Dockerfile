FROM python:3-slim


WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3-opencv
RUN apt-get install -y tesseract-ocr

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]

# docker build -t flask-server .
# docker run --rm -p 8080:8080 flask-server