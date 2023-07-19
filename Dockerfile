FROM python:3.11

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002
CMD ["python", "oidc.py"]