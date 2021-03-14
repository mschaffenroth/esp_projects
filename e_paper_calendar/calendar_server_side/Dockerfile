FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cal.py .
COPY Font.ttc .
COPY config.txt .
COPY may.jpg .

CMD [ "python", "./cal.py" ]
