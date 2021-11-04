FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY entrypoint.sh /
RUN apt-get update && apt-get install -y gettext
RUN chmod +x /entrypoint.sh
RUN pip install --upgrade pip
COPY ./predictsystems/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
CMD ["/entrypoint.sh"]
