FROM python:3.10

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# Install streamlit
RUN pip install streamlit

# Expose Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "/app/gui.py", "--server.enableCORS", "false"]
