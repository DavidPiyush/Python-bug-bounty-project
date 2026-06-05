import requests

# headers = {
#     "User-Agent":"Mozilla/5.0",
#     "X-Forwarded-For":"127.0.0.1",
#     "Authorization":"Bear YOURTOKEN",
#     "Referer":"https://google.com",
# }

# response = requests.get("https://httpbin.org/headers",headers=headers)

# print(response.json())


# payload = {
#     "username":"admin",
#     "password":"password123"
# }

# response = requests.post(
#     "https://httpbin.org/post",
#     json=payload
# )

# print(response.json())

# form_data = {
#     "username":"admin",
#     "password":"password123"
# }

# response = requests.post("https://httpbin.org/post",data=form_data)
# print(response.json())

'''

session = requests.Session()

login_response = session.post("https://httpbin.org/post",json={"username":"admin","password":"password"})

profile = session.get("https://httpbin.org/cookies")

session.cookies.set("session_id","Stolen_cookie_value")

session.headers.update({
    "Authorization":"Bearer token123"
})


print(profile.json())

'''

# response = requests.get("https://httpbin.org/response-headers?X-Custom=test")
response = requests.get("https://timesindian.com/")

if response.status_code == 200:
    print("Found it - endpoint exists and you have access")
elif response.status_code == 403:
    print("Exists but forbidden")
elif response.status_code == 401:
    print("Exists but need auth - find the token")
elif response.status_code == 404:
    print("Not found - or intentionally hidden")
elif response.status_code == 500:
    print("Server error")


print("\n--- Security Relevent Headers ---")
security_headers = [
    "Server",
    "X-Powered-By",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options"
]

for header in security_headers:
    value = response.headers.get(header,"MISSING ⚠️")
    print(f"{header}: {value}")