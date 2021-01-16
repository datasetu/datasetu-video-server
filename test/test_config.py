import json

ids = ["rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-1",
       "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-2",
       "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource-3"]

provider_url = 'https://auth.local:443/auth/v1/acl/set'
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

consumer_url = "https://auth.local:443/auth/v1/token"
consumer_certificate = '../datasetu-ca/consumer/consumer.pem'
consumer_key = '../datasetu-ca/consumer/consumer.key.pem'
consumer_credentials = (consumer_certificate, consumer_key)
consumer_body = json.dumps({
    "request": [
        {
            "id": ids[0],
            "scopes": ["write", "read"]
        },
        {
            "id": ids[1],
            "scopes": ["write", "read"]
        },
        {
            "id": ids[2],
            "scopes": ["write", "read"]
        },
        {
            "id": "rbccps.org/e096b3abef24b99383d9bd28e9b8c89cfd50be0b/example.com/test-category/test-resource.public",
            "scopes": ["write"]
        }
    ]
})

video = ['wKWldDnCZQ0.webm',
         'QXOXIMgHgZ0.mkv',
         'od5nla42Jvc.webm']

RECORD_SRC_DIR = '../nginx/record/'
