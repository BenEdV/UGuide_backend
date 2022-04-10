#!/bin/bash
# This script is a stress test which simulates calls being made to the server following a Poisson process
# usage ./stress_test.sh n l
# n is the total number of calls that are made
# l is the lambda parameter for the Poisson process, l=10 means that on average 10 calls are made per second

n=$1
lambda=$2

url="http://localhost:5000/{collection_id}"
token="{JWT_TOKEN}"
for ((i=0; i<n; i++))
do
	curl -s --request GET \
	  --url "$url/concepts/" \
	  --header "authorization: JWT $token" \
	  -w "$i GET concepts: \\t %{time_total} s %{http_code}\\n" --output /dev/null &
	pids[4*${i}]=$!

	# curl -s --request GET \
	#   --url "$url/groups/" \
	#   --header "authorization: JWT $token" \
	#   -w "$i GET groups:   \\t %{time_total} s %{http_code}\\n" --output /dev/null &
	# pids[4*${i}+1]=$!

	curl -s --request GET \
	  --url "$url/exams/" \
	  --header "authorization: JWT $token" \
	  -w "$i GET exams:    \\t %{time_total} s %{http_code}\\n" --output /dev/null &
	pids[4*${i}+2]=$!

	# curl -s --request GET \
	#   --url "$url/users/students" \
	#   --header "authorization: JWT $token" \
	#   -w "$i GET students: \\t %{time_total} s %{http_code}\\n" --output /dev/null &
	# pids[4*${i}+3]=$!

	# sleep until next call is made based on Poisson process
	sleep_time="$(awk -v seed=$RANDOM -v l="$lambda" 'BEGIN{ srand(seed); printf "%.8f", -log(rand())/l }')"
	echo "Sleeping for $sleep_time s"
	sleep "$sleep_time"
done

# wait for all pids
for pid in ${pids[*]}; do
    wait $pid
done
