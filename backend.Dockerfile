FROM python:3.12-slim 
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
EXPOSE 8000
# Step 7: Run FastAPI using uvicorn
CMD ["uvicorn", "app.endpoint.api:app", "--host", "0.0.0.0", "--port", "8000"]