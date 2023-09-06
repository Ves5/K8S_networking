FROM debian:bullseye-slim

# install ping and iperf3
RUN apt-get update && apt-get install -y iperf3 hping3

EXPOSE 5201

# run iperf3
ENTRYPOINT ["iperf3"]