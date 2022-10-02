# back_python


## Better to use the venv and vierutalenvwrapper
### For Local Environment:

Install requirements
`pip3 install -r requirements.txt`

#### Create a recipies.db file:
`python3 convert_json_to_db.py`

#### Run the API locally
`python3 recipy_api.py`

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
