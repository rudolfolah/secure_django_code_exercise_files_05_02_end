#!/usr/bin/env bash
source ./_setup.sh
http GET localhost:8000/api/v1/packages/ 'Authorization:@headers_auth.txt'
source ./_teardown.sh
