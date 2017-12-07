#!/bin/bash
# Frazier Baker
# Spark Cluster Start Script

echo $role
if [ "$role" = "MASTER" ]; then
  /spark/sbin/start-master.sh
fi


if [ "$role" = "WORKER" ]; then
  /spark/sbin/start-slave.sh spark://master:7077 -p 7078
fi
