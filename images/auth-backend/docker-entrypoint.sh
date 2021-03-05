#!/bin/ash

if [ $SKIP_TESTS == "true" ];
then
	python3 /root/auth-backend/auth-backend.py
else
	python3 test.py && python3 /root/auth-backend/auth-backend.py
fi
