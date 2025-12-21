FROM alpine:3.20

RUN apk add --no-cache \
    curl \
    bind-tools \
    busybox-extras \
    iproute2

# Keeps the pod alive; you exec in and run curl/dig/nslookup
CMD ["sh", "-c", "echo 'http-tester ready'; sleep infinity"]