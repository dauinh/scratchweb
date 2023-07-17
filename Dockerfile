FROM python:3.11

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "--app", "oidc", "run", "--host=0.0.0.0", "--port=5000", "--cert=adhoc", "--debug"]