FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/firebase.txt ./requirements/http.txt ./requirements/amqp.txt  ./
RUN pip install --no-cache-dir -r http.txt -r firebase.txt -r amqp.txt
COPY ./queue_logs_receiver/queue_logs_receiver.py ./
COPY ./key.json ./amqp_setup.py ../
CMD [ "python", "./queue_logs_receiver.py" ]