FROM golang:1.21 AS cloner

# Install git
RUN apt-get update && apt-get install -y git

# Set workdir
WORKDIR /app

# Clone repo (ganti URL dengan repo Anda)
RUN git clone https://github.com/aldinokemal/go-whatsapp-web-multidevice.git .

# Copy env file dari build context (jika ada)
COPY .env /go-whatsapp-web-multidevice/src/.env

# Build binary
# Fetch dependencies.

FROM golang:1.24-alpine3.20 AS builder
RUN apk update && apk add --no-cache gcc musl-dev gcompat
WORKDIR /whatsapp
COPY --from=cloner /app/src .

# Fetch dependencies.
RUN go mod download
# Build the binary with optimizations
RUN go build -a -ldflags="-w -s" -o /app/whatsapp

#############################
## STEP 2 build a smaller image
#############################
FROM alpine:3.20
RUN apk add --no-cache ffmpeg
WORKDIR /app
# Copy compiled from builder.
COPY --from=builder /app/whatsapp /app/whatsapp
# Run the binary.
ENTRYPOINT ["/app/whatsapp"]

CMD [ "rest" ]
