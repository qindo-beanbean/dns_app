FROM python:3.9-slim
WORKDIR /app
COPY fs.py /app/
RUN pip install flask requests
EXPOSE 9090
CMD ["python", "fs.py"]