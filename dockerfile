FROM python:3.9-slim

WORKDIR app/

COPY . .

RUN apt-get update 
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python3", "src/main.py"]