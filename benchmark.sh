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
    # IP=$(kubectl get pod -l app=iperf-server -o jsonpath="{.items[0].status.podIP}")
    
    # iperf3 TCP tests
    # echo -e "\n[TCP] starting pod-pod throughput tests\n"
    # for i in {1..5}; do
    #     echo "Iteration $i"
    #     kubectl exec -it ${POD} -- iperf3 -c $IP -O 2 | grep sender | awk '{print $7, $9}' >> $savefile
    #     sleep 1
    #     # returns sender throughput and retries
    # done
    # # sleep for 5 seconds
    # sleep 5

    # # iperf3 UDP tests
    # echo -e "\n[UDP] starting pod-pod throughput tests\n"
    # for i in {1..5}; do
    #     echo "Iteration $i"
    #     kubectl exec -it ${POD} -- iperf3 -c $IP -u -b 0| grep receiver | awk '{print $7, $9, $12}' >> $savefile
    #     sleep 1
    #     # returns receiver throughput, jitter and datagram loss
    # done
    # # sleep for 5 seconds
    # sleep 5

    # # Ping RTT tests
    # echo -e "\n[RTT] starting pod-pod latency tests\n"
    # for i in {1..5}; do
    #     echo "Iteration $i"
    #     kubectl exec -it ${POD} -- hping3 $IP -c 50 -i u20000 -1 | tail -1 | awk '{print $4}' >> $savefile
    #     sleep 1
    #     # returns just the values of min/avg/max from output of hping3 -> to be parsed later into csv
    # done
    # # sleep for 5 seconds
    # sleep 5

    # iperf3 pod-svc tests

    kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: iperf-server-tcp
spec:
  selector:
    app: iperf-server
  ports:
  - protocol: TCP
    port: 5201
    targetPort: 5201
EOF

    SVC_IP_TCP=$(kubectl get svc iperf-server-tcp -o jsonpath="{.spec.clusterIP}")
    

    echo -e "\n[TCP] starting pod-svc throughput tests\n"
    for i in {1..5}; do
        echo "Iteration $i"
        kubectl exec -it ${POD} -- iperf3 -c $SVC_IP_TCP -O 2 | grep sender | awk '{print $7, $9}' >> $savefile
        # returns sender throughput and retries
    done

    kubectl delete -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: iperf-server-tcp
spec:
  selector:
    app: iperf-server
  ports:
  - protocol: TCP
    port: 5201
    targetPort: 5201
EOF

    # sleep for 5 seconds
    sleep 5

    kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: iperf-server-udp
spec:
  selector:
    app: iperf-server
  ports:
  - protocol: UDP
    port: 5201
    targetPort: 5201
EOF

    SVC_IP_UDP=$(kubectl get svc iperf-server-udp -o jsonpath="{.spec.clusterIP}")

    echo -e "\n[UDP] starting pod-svc throughput tests\n"
    for i in {1..5}; do
        echo "Iteration $i"
        kubectl exec -it ${POD} -- iperf3 -c $SVC_IP_UDP -u -b 0 | grep receiver | awk '{print $7, $9, $12}' >> $savefile
        # returns receiver throughput, jitter and datagram loss
    done

    kubectl delete -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: iperf-server-udp
spec:
  selector:
    app: iperf-server
  ports:
  - protocol: UDP
    port: 5201
    targetPort: 5201
EOF

    echo -e "\nCleaning up $filename deployment"
    # clean after deployment
    kubectl delete --cascade -f $filename

    echo "Deployment cleaned up"
# done

echo "Tests done"