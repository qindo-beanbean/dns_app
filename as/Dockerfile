FROM python:3.9-slim
WORKDIR /app
COPY as.py /app/
# No need to install socket as it's a built-in module
EXPOSE 53533/udp
CMD ["python", "as.py"]