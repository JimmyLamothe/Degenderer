FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-w 4", "-k", "gevent", "-b :8080", "--timeout", "600", "app:app"]