#!/usr/bin/bash

set -eu
filename=deployments/deployment2.yaml
# for filename in deployments/*.yaml; do
    [ -e "$filename" ] || continue

    echo "Deploying $filename to cluster
    "
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
    echo "[TCP] starting throughput tests"
    for i in {1..5}; do
        ### to consider omitting first 1-2 seconds cause of TCP startup
        # tail commented to see if the TCP issue happens
        kubectl exec -it ${POD} -- iperf3 -c $IP $@ #| tail -4 | head -n 2
        # echo ""
    done

    # iperf3 UDP tests
    echo "[UDP] starting throughput tests"
    for i in {1..5}; do
        kubectl exec -it ${POD} -- iperf3 -c $IP -u -b 0 $@ #| tail -4 | head -n 2
    done

    # Ping RTT tests
    echo "[RTT] starting latency tests"
    for i in {1..5}; do
        kubectl exec -it ${POD} -- ping -c 100 -i 0.2 $IP | tail -1
        # echo ""
    done

    echo "Cleaning up $filename deployment"
    # clean after deployment
    kubectl delete --cascade -f $filename

    echo "Deployment cleaned up"
# done

echo "Tests done"