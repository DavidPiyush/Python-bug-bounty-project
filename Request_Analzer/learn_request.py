import requests


# GET Request
response = requests.get("https://www.geeksforgeeks.org/")

# print(response.status_code)
# print(response.headers)
# print(response.headers.get("Server"))


# Query Parameters
params = {
    "q": "test"
}

requests.get(
    "https://site.com/search",
    params=params
)


# Sending POST Data

data = {
    "username":"admin",
    "password":"admin"
}

# response = requests.post("https://site.com/login",data=data)


# JSON APIs

response = requests.get("https://www.geeksforgeeks.org/")
# data = response.json()
# print(data)

# Custom Headers

headers = {
    "User-Agent": "DavidScanner",
    "X-Forwarded-For": "127.0.0.1"
}

# response = requests.get(
#     url,
#     headers=headers
# )


# Mini Project: Endpoint Analyzer

urls = [
    "https://timesindian.com",
    "https://timesindian.com/login",
    "https://timesindian.com/admin"
]

for url in urls:
    try:
        response = requests.get(url,timeout=5)
        print({"url":url,"status":response.status_code,"Server":response.headers.get("Server")})
    except Exception:
        print(f"failed: {url}")