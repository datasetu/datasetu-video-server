from 	alpine:3.12.3

label 	maintainer="Poorna Chandra Tejasvi <pct@artpark.in"

copy 	requirements.txt /
copy 	docker-entrypoint.sh /

run	    apk update && \
	    apk add build-base python3 py3-pip python3-dev libffi-dev openssl openssl-dev && \
	    pip install -r requirements.txt

cmd     ./docker-entrypoint.sh
