FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/http.txt ./
RUN pip install --no-cache-dir -r http.txt
COPY ./weather_check/weather_check.py ./
CMD [ "python", "./weather_check.py" ]