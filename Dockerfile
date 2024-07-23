FROM python:3.12

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "qa_api.main:app", "--host", "0.0.0.0", "--port", "8000"]