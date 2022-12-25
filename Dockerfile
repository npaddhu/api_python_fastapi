FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#uvicorn app.main:app --host 0.0.0.0 --port 8000; you should seperate the elements for every space.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]  

