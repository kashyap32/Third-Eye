import requests,json
headers = {'Content-type':'application/json'}
imageurl = 'http://pngimg.com/uploads/orange/orange_PNG780.png'
data = {'url':imageurl}
res = requests.post('http://localhost:5432/api/v1/classify_image', data=json.dumps(data), headers=headers)
print(res.text)
