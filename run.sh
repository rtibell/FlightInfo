#!/bin/bash

for i in `seq 1 200`
do
  echo "Loop $i"
  /home/pi/dump1090/dump1090 --net --quiet &
  sleep 5
  python readFlightToFile.py
done

