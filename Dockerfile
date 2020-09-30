FROM python:3.7.4-stretch

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY braskomics.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP braskomics.py
EXPOSE 80

ENTRYPOINT ["./boot.sh"]
