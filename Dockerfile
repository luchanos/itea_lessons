FROM python:3.7.4
WORKDIR /
ADD . .
EXPOSE 6000:6000
RUN pip3 install -r requirements.txt
CMD ["sanic", "server.app", "--host=0.0.0.0", "--port=6000"]
