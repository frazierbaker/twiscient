#!/bin/ash
# Installing spark on Frazier's Cluster
################################################

# Run on Alpine 3.6

# install base packages
apk --update add bash curl util-linux coreutils binutils findutils grep procps openjdk8-jre

# download spark
curl -o /spark.tgz http://mirrors.ibiblio.org/apache/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz

# move spark to spark folder
mv ./spark-* /spark
