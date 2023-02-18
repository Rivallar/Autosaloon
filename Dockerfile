FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONYWRITEBYTECODE=1
WORKDIR /autosaloon_app
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy