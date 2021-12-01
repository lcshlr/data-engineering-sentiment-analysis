FROM python:3.6
WORKDIR /api
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY * ./
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]