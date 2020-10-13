FROM python:3
ADD main.py /
ADD testing.py /
ADD test.xml /
RUN pip3 install pandas
ENTRYPOINT [ "python3", "main.py" ]
