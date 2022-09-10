FROM python

WORKDIR /inside_test

COPY app app/

RUN pip install -r app/requirements.txt

EXPOSE 8100

CMD [ "python", "app/run.py" ]