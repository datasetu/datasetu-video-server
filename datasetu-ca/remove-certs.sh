#!/bin/bash

#Delete resource server certificates
rm -f 	resource-server/resource-server.csr	    	\
    	resource-server/resource-server.key.pem		\
    	resource-server/resource-server.pem		2>/dev/null

#Remove provider certificates
rm -f 	provider/provider.csr		    		\
    	provider/provider.pem		    		\
    	provider/provider.key.pem 			2>/dev/null

#Remove consumer certificates
rm -f 	consumer/consumer.csr		    		\
    	consumer/consumer.pem		    		\
    	consumer/consumer.key.pem 			2>/dev/null

#Remove self-signed SSL certs
rm -f	../datasetu-auth-server/https-key.pem		\
    	../datasetu-auth-server/https-certificate.pem	\
    	../datasetu-auth-server/ca.datasetu.org.crt	\
    	../datasetu-auth-server/ca.key			\
    	../nginx/nginx-ssl.pem				\	
    	../nginx/nginx-ssl.key.pem			\
    	../auth-backend/resource-server.p12		2>/dev/null

