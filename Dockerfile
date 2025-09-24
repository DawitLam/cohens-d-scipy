# Multi-stage Docker setup for cross-platform testing

# Ubuntu testing
FROM python:3.11-slim as ubuntu-test
WORKDIR /app
COPY cohens_d_package/ ./cohens_d_package/
COPY intensive_testing/ ./intensive_testing/
RUN cd cohens_d_package && pip install -e ".[test]"
CMD ["python", "-m", "pytest", "cohens_d_package/tests/", "-v"]

# Alpine Linux testing (smaller, different libc)
FROM python:3.11-alpine as alpine-test  
WORKDIR /app
RUN apk add --no-cache gcc musl-dev
COPY cohens_d_package/ ./cohens_d_package/
COPY intensive_testing/ ./intensive_testing/
RUN cd cohens_d_package && pip install -e ".[test]"
CMD ["python", "-m", "pytest", "cohens_d_package/tests/", "-v"]

# Test runner
FROM ubuntu-test as test-runner
COPY docker-test.sh /docker-test.sh
RUN chmod +x /docker-test.sh
CMD ["/docker-test.sh"]