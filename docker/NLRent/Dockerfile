# FROM python:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./manage.py", "runserver" ]

FROM python
COPY . .
EXPOSE 8000
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]