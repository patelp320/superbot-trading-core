FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install schedule yfinance pandas

CMD ["python3", "main.py"]
