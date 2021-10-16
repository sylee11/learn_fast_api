FROM python:3.9
WORKDIR /fastapi
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
#RUN pipenv install --deploy --ignore-pipfile
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . .
#EXPOSE 5000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
