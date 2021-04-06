#!/bin/bash

#Generate self-signed SSL certificate for auth server
openssl req -newkey rsa:2048 -nodes -keyout ../datasetu-auth-server/https-key.pem -x509 -days 365 -out ../datasetu-auth-server/https-certificate.pem -subj "/CN=auth.local"

#Generate self-signed SSL certificate for nginx
#TODO: Replace with 'SERVER_NAME' Do not hardcode value
openssl req -newkey rsa:2048 -nodes -keyout ../nginx/nginx-ssl.key.pem -x509 -days 365 -out ../nginx/nginx-ssl.pem -subj "/CN=video.datasetu.org"

#Generate self-signed CA certificate
openssl req -x509 -nodes -days 365 -subj "/CN=ca.datasetu.org/emailAddress=ca@datasetu.org" -newkey rsa:2048 -keyout ../datasetu-auth-server/ca.key -out ../datasetu-auth-server/ca.datasetu.org.crt

#Generate consumer's CSR
openssl req -new -newkey rsa:2048 -nodes -out consumer/consumer.csr -keyout consumer/consumer.key.pem -subj "/CN=individual/emailAddress=consumer@iisc.ac.in/id-qt-unotice=class:2"

#Generate provider's CSR
openssl req -new -newkey rsa:2048 -nodes -out provider/provider.csr -keyout provider/provider.key.pem -subj "/CN=employee/emailAddress=provider@rbccps.org/id-qt-unotice=class:3"

#Generate resource server's CSR
openssl req -new -newkey rsa:2048 -nodes -out resource-server/resource-server.csr -keyout resource-server/resource-server.key.pem -subj "/CN=example.com/id-qt-unotice=class:1/emailAddress=provider@rbccps.org"

#Sign consumer's CSR
openssl x509 -CA ../datasetu-auth-server/ca.datasetu.org.crt -CAkey ../datasetu-auth-server/ca.key -CAcreateserial -in consumer/consumer.csr -req -days 365 -sha256 -out consumer/consumer.pem

#Sign provider's CSR
openssl x509 -CA ../datasetu-auth-server/ca.datasetu.org.crt -CAkey ../datasetu-auth-server/ca.key -CAcreateserial -in provider/provider.csr -req -days 365 -sha256 -out provider/provider.pem 

#Sign resource server's CSR
openssl x509 -CA ../datasetu-auth-server/ca.datasetu.org.crt -CAkey ../datasetu-auth-server/ca.key -CAcreateserial -in resource-server/resource-server.csr -req -days 365 -sha256 -out resource-server/resource-server.pem 

cp resource-server/resource-server.pem resource-server/resource-server.key.pem ../auth-backend/
