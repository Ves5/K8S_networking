#!/usr/bin/bash

set -eu

savefile=results/${1-$(date +"%Y-%m-%d-%H-%M-%S")}.txt

filename=deployments/deployment.yaml
# for filename in deployments/*.yaml; do
    [ -e "$filename" ] || continue

    echo -e "\nDeploying $filename to cluster"
    # set up deployment
    kubectl create -f $filename

    # wait for server to start
    until $(kubectl get pods -l app=iperf-server -o jsonpath='{.items[0].status.containerStatuses[0].ready}'); do
        echo "Waiting for iperf3 server to start..."
        sleep 5
    done
    echo "iperf-server is running"

    #wait for client to start
    until $(kubectl get pods -l app=iperf-client -o jsonpath='{.items[0].status.containerStatuses[0].ready}'); do
        echo "Waiting for iperf3 client to start..."
        sleep 5
    done
    echo "iperf-client is running"

    # run few iperf tests to get average
    POD=$(kubectl get pod -l app=iperf-client -o jsonpath="{.items[0].metadata.name}")
    IP=$(kubectl get pod -l app=iperf-server -o jsonpath="{.items[0].status.podIP}")
    # echo "Using pod $POD for tests"
    
    # iperf3 TCP tests
    echo -e "\n[TCP] starting throughput tests\n"
    for i in {1..5}; do
        echo "Test $i"
        kubectl exec -it ${POD} -- iperf3 -c $IP -O 2 | tail -3 | head -n 1 | awk '{print $7}' >> $savefile
        # returns receiver throughput
    done

    # iperf3 UDP tests
    echo -e "\n[UDP] starting throughput tests\n"
    for i in {1..5}; do
        echo "Test $i"
        kubectl exec -it ${POD} -- iperf3 -c $IP -u -b 1000m | tail -3 | head -n 1 | awk '{print $7 $9 $11}' >> $savefile
        # returns receiver throughput, jitter and datagram loss
    done

    # Ping RTT tests
    echo -e "\n[RTT] starting latency tests\n"
    for i in {1..5}; do
        echo "Test $i"
        kubectl exec -it ${POD} -- hping3 $IP -c 100 --faster -1 | tail -1 | awk '{print $4}' >> $savefile
        # returns just the values of min/avg/max from output of hping3 -> to be parsed later into csv
    done

    echo -e "\nCleaning up $filename deployment"
    # clean after deployment
    kubectl delete --cascade -f $filename

    echo "Deployment cleaned up"
# done

echo "Tests done"