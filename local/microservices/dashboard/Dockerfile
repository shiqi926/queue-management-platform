FROM python:3
WORKDIR /usr/src/app
COPY ./requirements/http.txt ./
RUN pip install --no-cache-dir -r http.txt 
COPY ./dashboard/dashboard.py ./
CMD [ "python", "./dashboard.py" ]