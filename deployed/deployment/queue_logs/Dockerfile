FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/firebase.txt ./requirements/http.txt ./requirements/pubsub.txt ./
RUN pip install --no-cache-dir -r http.txt -r firebase.txt -r pubsub.txt
ENV PYTHONUNBUFFERED True
COPY ./queue_logs/queue_logs.py ./
COPY ./key.json ../
CMD [ "python", "./queue_logs.py" ]