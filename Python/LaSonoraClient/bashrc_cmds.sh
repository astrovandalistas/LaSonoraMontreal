## S&S
isrun=`ps -u pi | grep python | wc -l`
if [ $isrun -lt 1 ] 
then 
    cd /home/pi/Dev/LaSonoraTelematica/Python/LaSonoraClient
    export DISPLAY=":0.0"
    startx &
    rm -rf ./stop.sh
    while [ ! -f ./stop.sh ]
    do
	python LaSonoraClient.py
	killpid=$!
	sleep 600
	kill -9 $killpid
    done
    rm -rf ./stop.sh
    sudo halt -n
fi
