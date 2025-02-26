FROM python:3.10

WORKDIR /app
COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
#COPY run_migrations.sh /app/run_migrations.sh
#RUN chmod +x /app/run_migrations.sh
#RUN /app/run_migrations.sh

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]