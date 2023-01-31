#!/bin/bash

ans=""

while read line;do
    eval "$line"
done < /root/ai-tools/recogcap/etc/recogcap-s.conf

if [ -n "$host" ];then
    ans=$ans"--host "
    ans=$ans$host
    ans=$ans" "
fi
if [ -n "$port" ];then
    ans=$ans"--port "
    ans=$ans$port
    ans=$ans" "
fi
if [ -n "$model" ];then
    ans=$ans"--model "
    ans=$ans$model
    ans=$ans" "
fi
if [ -n "$model_path" ];then
    ans=$ans"--model_path "
    ans=$ans$model_path
    ans=$ans" "
fi
if [ -n "$cap_array" ];then
    ans=$ans"--cap_array "
    ans=$ans$cap_array
    ans=$ans" "
fi
echo "config : "$ans
recogcap-s $ans
