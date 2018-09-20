# Buffer-python

Buffer-python is an API wrapper for the API v1 of Buffer written in Python

## Installing
```
pip install buffer-python-lib
```

## Usage
```
from buffer.client import Client

client = Client('CLIENT_ID', 'CLIENT_SECRET')
```

Get authorization url
```
url = client.get_authorization_url('REDIRECT_URL')
```

Exchange the code for an access token
```
token = client.exchange_code('REDIRECT_URL', 'CODE')
```

Set the access token
```
client.set_token('TOKEN')
```

Get user information
```
account = client.get_user_info()
```

Get user registered profiles
```
profiles = client.get_user_profiles()
```

Get specific user profile
```
profile = client.get_specific_profile('PROFILE_ID')
```

Get leads given the form
```
posting_schedules = client.get_posting_schedules('PROFILE_ID')
```

Get sent posts
```
sent_posts = client.get_sent_post('PROFILE_ID')
```

Get specific post
```
specific_post = client.get_specific_post('POST_ID')
```

New post or update
```
post = client.new_post('PROFILE_ID', 'TEXT', True)
```

## Requirements
- requests

## TODO
- unittest
