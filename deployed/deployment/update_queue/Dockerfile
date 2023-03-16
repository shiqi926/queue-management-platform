FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/http.txt ./requirements/pubsub.txt ./
RUN pip install --no-cache-dir -r http.txt -r pubsub.txt
COPY ./update_queue/update_queue.py ./
CMD [ "python", "./update_queue.py" ]