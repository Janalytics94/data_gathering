FROM python:3.10-slim-buster

WORKDIR /usr/src/app

COPY . /usr/src/app/

VOLUME [ "/usr/src/app/sut/logs" ]

EXPOSE 5000

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app.py"]

