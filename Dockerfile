FROM python:3.6-stretch
WORKDIR /project
ADD . /project
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD ["python","app.py"]