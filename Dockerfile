FROM python:3.6.8-slim
WORKDIR /mednickdb
ADD setup_env.sh  .
ADD requirements.txt .
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git
RUN pip install -r requirements.txt
#ENV pyparse mednickdb_pyparse/mednickdb_pyparse
#RUN mv src/mednickdb-pyparse mednickdb_pyparse
#RUN mv src/mednickdb-pysleep
#RUN chmod +x ./setup_env.sh
RUN sh setup_env.sh
ENV MEDNICKDB_DEFAULT_PW Nap4life!!!
#VOLUME mednickdb_pyparse/uploads/
#CMD ["python", "mednickdb_pyparse/mednickdb_auto_parse.py"]
