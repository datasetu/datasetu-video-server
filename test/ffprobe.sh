#!/bin/bash

success=0
i=0
while [ $i -le 20 ]
do
  timeout 2 ffprobe -v quiet -print_format json -show_streams   "rtmps://localhost:1935/rtmp/rbccps.org%2Fe096b3abef24b99383d9bd28e9b8c89cfd50be0b%2Fexample.com%2Ftest-category%2Ftest-resource-1?token=auth.local%2Fbb438f011b9e04d610da09f78a0ac099"

  if [ $? -eq 0 ]
  then
    ((success++))
  fi
  ((i++))
done
echo $success
