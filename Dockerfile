FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir streamlit pandas numpy scikit-learn matplotlib tensorflow

EXPOSE 8501

CMD ["streamlit", "run", "gui_control.py", "--server.enableCORS", "false"]
