FROM python:3.12.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN playwright install --with-deps

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]