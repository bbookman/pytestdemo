FROM python:3.9.7-buster
RUN mkdir maritime_20_test_suite
COPY . /maritime_20_test_suite
WORKDIR /maritime_20_test_suite/functional_tests
RUN pip install --no-cache-dir -r requirements.txt
CMD ["pytest", "tests"]
