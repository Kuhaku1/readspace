FROM python:3
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
ADD pip.conf /root/.pip/
RUN pip3 install -r /app/requirements.txt

WORKDIR /app
ADD . /app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]