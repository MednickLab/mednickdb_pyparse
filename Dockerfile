FROM python:3.6.8
COPY requirements.txt requirements.txt
#COPY requirements_pip.txt requirements_pip.txt
WORKDIR .
RUN apt-get update && apt-get upgrade  
#apt-get install -y git
#RUN while read requirement; do conda install --yes $requirement; done < requirements.txt
RUN pip install -r requirements.txt
COPY . .
VOLUME mednickdb_pyparse/uploads/
#CMD ["python", "mednickdb_pyparse/mednickdb_auto_parse.py"]
CMD echo "hello world"
