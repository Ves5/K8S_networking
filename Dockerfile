FROM alpine:3.18

# install ping and iperf3
RUN apk update && apk upgrade && apk add --no-cache iperf3
# allow ping to be use in the container
RUN chmod 4755 /bin/ping

EXPOSE 5201

# run iperf3
ENTRYPOINT ["iperf3"]