# kill pid
kill -s 9 $1

#check ping 
#ping
return_code=1
ping_times=0
while [ $return_code -ne 0 ]; do
        date
        ping -c 4 www.baidu.com
        return_code=$?
        ((ping_times=ping_times+1))
        if [ $return_code -ne 0 ]; then
                echo "ping times : $ping_times"
                sleep 4s
        fi
done

#reboot
sleep 3s
python $2/main.py > log.txt &
