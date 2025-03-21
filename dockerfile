FROM python:3.12
WORKDIR /user/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py ./api.py
COPY create_db.py ./create_db.py

EXPOSE 9090

RUN python create_db.py

ENV FLASK_APP=api.py

ENV FLASK_RUN_PORT=9090

CMD ["flask", "run", "--host=0.0.0.0"]