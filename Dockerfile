# Used instead of official python image to use the hot-reload on python files
FROM nikolaik/python-nodejs:latest
# Remove before production
RUN npm install -g nodemon

COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
ADD fredo /app/fredo

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "nodemon", "fredo/main.py"]