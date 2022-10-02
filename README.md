# back_python


## Better to use the venv and vierutalenvwrapper

Install requirements
`pip3 install -r requirements.txt`

Run the API locally
`/home/mea/.virtualenvs/hungrysquad/bin/python /home/mea/Dev/Project/recipy-api.py`

Test POST
```
curl http://localhost:5000/posts \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
    "name": "Borsh",
    "source": "url",
    "image": "image",
    "time":"lol",
    "servings": "2",
    "description":"Lol",
    "ingredients":"1/n2/n3",
    "nutrients": "1/n2/n3"
}'
```
Test PATCH
```
curl http://localhost:5000/posts/1 \
    -X PATCH \
    -H "Content-Type: application/json" \
    -d '{"name":"Chocolate", "ingredients":"L"}
```
Test GET in browser or REST API application (like POSTMAN):
```
http://localhost:5000/posts/
```
