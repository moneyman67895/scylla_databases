FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY /load_data /app
COPY /load_data/data_csvs /app/data_csvs
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["soil_data.py"]
