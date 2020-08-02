FROM python:alpine3.12 as Builder

ADD requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

ADD ./*.py ./

EXPOSE 80
CMD [ "python", "./main.py" ]