FROM python:3.11.6 as base
RUN apt install -y wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
RUN dpkg -i cuda-keyring_1.1-1_all.deb
RUN apt update && apt install -y cuda


FROM base
WORKDIR /makeup_removal

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit","run", "src/main.py"]