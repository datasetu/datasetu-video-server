#!/bin/bash

openssl pkcs12 -inkey private-key.pem -in resource-server.pem -export -out certificate.pem.p12
