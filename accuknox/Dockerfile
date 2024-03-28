FROM python:3.9
WORKDIR /app
COPY requirements .
RUN pip3 install --upgrade pip && pip install --upgrade pip setuptools wheel && pip3 install numpy && pip install gunicorn
RUN pip3 install -r requirements
COPY . .
EXPOSE 8000
RUN chmod +x /app/runner.sh
CMD ["/app/runner.sh"]
