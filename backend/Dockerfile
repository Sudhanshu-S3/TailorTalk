FROM python:3.9-slim

WORKDIR /code


COPY req.txt .


RUN pip install --no-cache-dir -r req.txt


COPY ./app ./app
COPY credentials.json .


EXPOSE 8000

ENV PYTHONPATH=/code

# Run app.main when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
