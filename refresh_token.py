import requests

url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type" : "refresh_token",
    "client_id"  : "3b34f2e7f557ef84bf043fccf76e1791",
    "refresh_token" : 'tqUBFnFzaODG6Z1XTFEsQ2WlQjfG-2r6JpI1JQUtCioljgAAAYiWajCL'
}
response = requests.post(url, data=data)

print(response.json())