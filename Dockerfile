FROM python:latest

RUN python3 -m pip install flask gunicorn humanfriendly

WORKDIR /root
COPY . /root

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

EXPOSE 5000
