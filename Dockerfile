FROM python

COPY requirements.txt .
RUN pip install -r requirements.txt && mkdir /app
WORKDIR /app
CMD ["python", "app.py"]
COPY . /app
