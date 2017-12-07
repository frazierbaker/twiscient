#!/bin/bash
PREFIX=`date | md5sum | cut -d' ' -f1`
MYDIR="$PREFIX-twiscient-run"
BACKUP=`date | md5sum | md5sum | cut -d' ' -f1`

cp -r ../data/twitter ./twitter

mv twitter-parallel twitter-parallel-$BACKUP || echo "Directory twitter-parallel does not already exist... No backup created."
cp -r twitter twitter-parallel
time PARALLEL=1 spark-submit ./twiscient.py 2>>parallel.err >>parallel.out

mv twitter-sequential twitter-sequential-$BACKUP || echo "Directory twitter-sequential does not already exist... No backup created."
cp -r twitter twitter-sequential
time SEQUENTIAL=1 ./twiscient.py 2>>sequential.err >sequential.out

mv twitter-annotated twitter-annotated-$BACKUP || echo "Directory twitter-annotated does not already exist... No backup created."
cp -r twitter twitter-annotated
time ./twiscient.py 2>>annotated.err >>annotated.out

mkdir $MYDIR
mv twitter-annotated $MYDIR
mv twitter-sequential $MYDIR
mv twitter-parallel $MYDIR
mv *.out $MYDIR
mv *.err $MYDIR

echo "Done."
