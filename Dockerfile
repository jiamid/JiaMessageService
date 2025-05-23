FROM python:3.12
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN rm -f /etc/localtime
RUN  ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

COPY . /code/