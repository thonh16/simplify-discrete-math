FROM alpine:3.14

COPY ./dist/app /app

CMD ["/app"]