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

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.
#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/buffer-python/issues).
#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/buffer-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
