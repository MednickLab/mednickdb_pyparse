echo "start setup microservice environment"
Pyparse=mednickdb_pyparse
#mv src/mednickdb-pyparse/mednickdb_pyparse $Pyparse
#mv src/mednickdb-pyparse/tests tests
echo "finished pyparse"
mv src/mednickdb-pysleep/mednickdb_pysleep $Pyparse/mednickdb_pysleep
echo "finished pysleep"
mv src/mednickdb-pyapi/mednickdb_pyapi/* $Pyparse/
echo "finished pyapi"
rm -rf src
echo "done"
