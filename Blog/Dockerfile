FROM python:3.8.10-alpine


WORKDIR /Blog/


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN pip install django-utils-six



COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh


COPY . .


ENTRYPOINT ["./entrypoint.sh"]