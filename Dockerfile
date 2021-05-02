FROM python:3.6-stretch
WORKDIR /project
ADD . /project
RUN pip3 install -r requirements.txt
EXPOSE 8080
CMD ["python3","app.py"]