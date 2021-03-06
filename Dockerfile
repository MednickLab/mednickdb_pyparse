FROM python:3.6.8-slim
WORKDIR /mednickdb
ADD setup_env.sh  .
ADD requirements.txt .
ADD mednickdb_pyparse mednickdb_pyparse
ADD tests tests
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git tzdata
ENV TZ America/Los_Angeles
RUN pip install -r requirements.txt
RUN sh setup_env.sh
ENV MEDNICKDB_DEFAULT_PW Nap4life!!!
#VOLUME mednickdb_pyparse/uploads/
CMD ["python", "mednickdb_pyparse/mednickdb_auto_parse.py"]
