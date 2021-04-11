
FROM python:3-alpine

COPY requirements-base.txt requirements.txt /
RUN pip install -r /requirements.txt

COPY . /eng_zap_challenge_python
WORKDIR /eng_zap_challenge_python

EXPOSE 5000
RUN chmod +x gunicorn.sh
ENTRYPOINT ["./gunicorn.sh"]