FROM python:3.6
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY run.sh .
RUN sh run.sh
ADD . .
WORKDIR /app/spider
CMD python3 run.py