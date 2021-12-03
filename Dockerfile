FROM python:3.10
WORKDIR /app
COPY ./requirments.txt /app/requirments.txt
RUN cd /app && pip3 install -r /app/requirments.txt
CMD ["python3", "/app/app.py"]

