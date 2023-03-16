FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/http.txt ./
RUN pip install --no-cache-dir -r http.txt
COPY ./view_status/view_status.py ./
COPY ./key.json ../
CMD [ "python", "./view_status.py" ]