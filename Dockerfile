FROM mednickdb/pyapi:latest
WORKDIR /pyparse
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y git
COPY . .
RUN pip install -r requirements.txt
VOLUME mednickdb_pyparse/uploads/
#CMD ["python", "mednickdb_pyparse/mednickdb_auto_parse.py"]
CMD ls
