# kill pid
kill -s 9 $1
#reboot
sleep 3s
python $2/main.py > log.txt &
