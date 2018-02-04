#!/bin/bash


md5_str=$1
path=$2


echo $md5_str

for i in {1..10}
 do 
   ssh_pid=`ps -ef|grep "$md5_str"|grep -v grep|grep -v sshpass|grep -v $0|awk '{print $2}'`
   echo "found the pid $ssh_pid"	
   
   if [ "$ssh_pid" = "" ];then
      echo "not fount the pid"
      sleep 1
      continue
     
   else
         
       work_dir='./log/audit'
     if [ -d $2 ];then
         #mkdir -p $path
         echo "start ---loging0----"
     else
       mkdir -p $2
     fi
       

     strace -f -p $ssh_pid -o "$2/$md5_str.log"
     echo $2 >> /tmp/aa
     break 

     



   fi
   
done	
