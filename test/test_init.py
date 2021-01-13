import requests, os, youtube_dl, json
from urllib.parse import quote_plus
import test-video-server

id = ["rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-1",
	  "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-2",
	  "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-3"]
	  # "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-~!@#$%^^&*()_+{}|:<>?,./;'[]=-`resource-4"]

provider_url = 'https://localhost:8443/auth/v1/acl/set'
provider_certificate = '../datasetu-ca/provider/provider.pem'
provider_key = '../datasetu-ca/provider/provider.key.pem'
provider_credentials = (provider_certificate, provider_key)
provider_body = json.dumps(
	{
		"policy": "consumer@iisc.ac.in can access example.com/test-category/test-resource-1 for 1 month;" +
				  "consumer@iisc.ac.in can access example.com/test-category/test-resource-2 for 1 month;" +
				  "consumer@iisc.ac.in can access example.com/test-category/test-resource-3 for 1 month;" +
				  "consumer@iisc.ac.in can access example.com/test-category/test-resource.public for 1 month"
	}
)

consumer_url = "https://localhost:8443/auth/v1/token"
consumer_certificate = '../datasetu-ca/consumer/consumer.pem'
consumer_key = '../datasetu-ca/consumer/consumer.key.pem'
consumer_credentials = (consumer_certificate, consumer_key)
consumer_body = json.dumps({
	"request": [
		{
			"id": id[0],
			"scopes": ["write", "read"]
		},
		{
			"id": id[1],
			"scopes": ["write", "read"]
		},
		{
			"id": id[2],
			"scopes": ["write", "read"]
		},
		# {
		# 	"id": id[3],
		# 	"scopes": ["write", "read"]
		# },
		{
			"id": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource.public",
			"scopes": ["write"]
		}
	]
})

requests.post(
    url = provider_url,
    verify = False,
    cert = provider_credentials,
    data=provider_body,
    headers	= {"content-type":"application/json"}
)

resp = requests.post(
    url = consumer_url,
    verify = False,
    cert = consumer_credentials,
    data=consumer_body,
    headers	= {"content-type":"application/json","Host": "auth.local"}
)

for i in range(len(id)):
    id[i] = quote_plus(id[i])

token = quote_plus(resp.json()['token'])

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=wKWldDnCZQ0'])
    ydl.download(['https://www.youtube.com/watch?v=QXOXIMgHgZ0'])

# os.remove('Asha _ ARTPARK _ Bengaluru Tech Summit 2020-wKWldDnCZQ0.webm')
# os.remove('Talk by Prof  Bharadwaj Amrutur on AI & Robotics Technologies Park ARTPark   a new IISc initiative-QXOXIMgHgZ0.mkv')
