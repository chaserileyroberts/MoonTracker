# Allows us to use ctrl+c to exit both the 
# texter and the website server.
trap 'kill $BGPID; exit' SIGINT

python3 ./texter.py &
BGPID=$!
python3 app.py

# Kill texting service if the website crashes.
kill $BGPID