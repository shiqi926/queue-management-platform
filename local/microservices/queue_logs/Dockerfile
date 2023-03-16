FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/firebase.txt ./requirements/http.txt ./
RUN pip install --no-cache-dir -r http.txt -r firebase.txt 
COPY ./queue_logs/queue_logs.py ./
COPY ./key.json ../
CMD [ "python", "./queue_logs.py" ]