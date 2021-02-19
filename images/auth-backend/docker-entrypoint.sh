#!/bin/bash

if [ $SKIP_TESTS == "true" ];
then
	python3 app.py
else
	python3 test_authenticator.py && \
		python3 app.py
fi
