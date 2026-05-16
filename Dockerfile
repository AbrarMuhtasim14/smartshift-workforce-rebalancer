FROM python:3.11

WORKDIR /code

# Copy the entire monorepo into the container
COPY . /code

# Install dependencies specifically from the backend folder
RUN pip install --no-cache-dir --upgrade -r /code/backend/requirements.txt

# Move inside the backend folder to run the application
WORKDIR /code/backend

# Hugging Face requires your app to run on port 7860
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
