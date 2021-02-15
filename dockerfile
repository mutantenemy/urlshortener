FROM python:3.8

RUN pip install flask

RUN pip install flask_wtf

RUN pip install mechanize

COPY . .

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]