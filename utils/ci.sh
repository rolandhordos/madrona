# $WORKSPACE
# $JOB_NAME
echo 
echo 
echo Testing Madrona : revision $GIT_REVISION
echo
echo
coverage run run_tests.py

echo 
echo 
echo Building Madrona docs : revision $GIT_REVISION
echo
echo
python build_docs.py -d /var/www/madrona-docs -j  /usr/local/jsdoc-toolkit-read-only/jsdoc-toolkit 

echo 
echo 
echo Analyzing coverage : revision $GIT_REVISION
echo
echo
coverage xml --omit /usr/share

