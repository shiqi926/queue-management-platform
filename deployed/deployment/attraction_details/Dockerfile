FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/firebase.txt ./requirements/http.txt ./
RUN pip install --no-cache-dir -r firebase.txt -r http.txt
COPY ./attraction_details/attraction_details.py ./
COPY ./key.json ../
CMD [ "python", "./attraction_details.py" ]