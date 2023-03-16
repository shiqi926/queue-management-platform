FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/http.txt ./requirements/amqp.txt ./
RUN pip install --no-cache-dir -r http.txt -r amqp.txt
COPY ./update_queue/update_queue.py ./
COPY ./amqp_setup.py ../
CMD [ "python", "./update_queue.py" ]