FROM python:3.9.12

WORKDIR /src

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "flask", "--app" , "src", "run","--debug","--host=0.0.0.0"]