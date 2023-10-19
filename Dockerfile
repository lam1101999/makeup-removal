FROM python:3.11.6

WORKDIR /makeup_removal

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit","run", "src/main.py"]