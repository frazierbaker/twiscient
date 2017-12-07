# Twiscient
Parallelized Twitter Sentiment Analysis Using Apache Spark

## Background
This was a project for my [Parallel Computing Class (CS 5058 at the University of Cincinnati)](https://compuzzle.wordpress.com/parallel-programming/) where I decided to build a cluster in my basement and run sentiment analysis using Apache Spark.  I decided to make my code available to help other people trying to build clusters in their respective basements or run parallelized sentiment anlaysis on Twitter data.  Enjoy and let me know if you have any questions!

## Stack
I used [Alpine Linux](https://alpinelinux.org/) for this project.  I was familiar with Alpine from my experiences with Docker, and I was aiming for something lightweight to squeeze as much computing power out of my old machines as I could, so something the size of say, Ubuntu, wasn't going to cut it.
I used the standalone version of Spark and as you can see from my source code, for my analysis I relied heavily on pyspark.  The setup directory contains some scripts to get you going.
I also used the [Stanford CoreNLP Library](https://stanfordnlp.github.io/CoreNLP/), which relies on Java.  Again, the setup scripts should help you with installing these.

## Getting Started
My recommendation for starting out: look in the setup directory of this repo.  Take an old computer, wipe it clean (perhaps literally and figuratively) and install Alpine Linux on it.  Get it connected to the interwebs any way you see fit (I put my cluster behind a proxy for the sake of security).  Then, download the setup directory from this repo and run

```./install_spark.sh```

That should get you everything you need to download and run:

```role=MASTER ./start.sh```.

If you have additional machines, great!  Repeat the process, only this time, run

```MASTER=X.X.X.X role=WORKER ./start.sh```

 where the X's in `MASTER=X.X.X.X` are replaced by the IP address of your master machine.  If you don't have additional machines, that's okay, too!  You can still run pyspark on just the master node, though obviously it can only use the resources on the master machine until you set it up with another machine.
 
 If all you wanted to do was use Apache Spark, then everything should be set up and ready to go for you.  If you're interested in downloading twitter data, check out the data directory.  I have a download script in there that you might find helpful.  If you are interested in the Stanford CoreNLP library, check out the analysis scripts.  I also highly recommend you refer to [their documentation](https://stanfordnlp.github.io/CoreNLP/), as I only used a small portion of their library.
 
### Want to Know More About Twiscient?
If you want to know more about the project I submitted for my class, you can check out the PDFs in this repo.  They include my presentation and my report for the class.
