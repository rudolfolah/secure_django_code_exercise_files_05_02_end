#!/usr/bin/env bash
API_USERNAME=admin
API_PASSWORD=admin
TOKEN=$(http --print=b POST localhost:8000/oauth/token/ 'client_id=wql5aqXepfkcF0JQOAoOo921zbvcrQSg1MUb2VUe' 'client_secret=tVnwobvL4C7D76AOsYkrtDLh1D1mahbUqkzSBfqVi2zXfsBBD9Jm8FNe6yWof1XYIOwBfxtKrZh4Eug3piGu94Oga2R0VHJVG2VxQn1pw5Y5xcBOva0IX1n4WrPXZn0N' 'grant_type=password' "username=$API_USERNAME" "password=$API_PASSWORD" | python -c "import sys, json; data = json.load(sys.stdin); print(data['access_token'])")
echo "Bearer $TOKEN" > headers_auth.txt
