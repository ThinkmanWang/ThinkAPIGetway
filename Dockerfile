FROM python:3.9.6
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt -i https://pypi.douban.com/simple

RUN mkdir /app
COPY . /app
WORKDIR /app
CMD python main.py
