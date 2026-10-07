# Cloud Nation | Docker Class
FROM python:3.9

MAINTAINER Mohammed Mubashir <cloudnation46@gmail.com>

COPY . /app/

WORKDIR /app/

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "app.py" ]
