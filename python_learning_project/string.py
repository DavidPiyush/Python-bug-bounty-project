url = "https://api.example.com/login"

# print(len(url))
# print(url[0])
# print(url[-1])

header = 'CONTENT-TYPE'
# print(header.lower())

header = 'content-type'
# print(header.upper())

token = " admin "
# print(token.strip())

parts = url.split("/")[2]
# print(parts)

words = ['admin','panel',"David"]

result = "/".join(words)
# print(result)

# if "login" in url:
    # print("Found")


keywords = [
    "admin","login",'dashboard','upload'
]

url = url.replace("http://","https://")
# print(url)

url = "https://example.com/profile?id=1"
base = url.split("?")[0]
# print(base)

query = url.split("?")[1]
# print(query)

param = query.split("=")[0]
# print(param)

# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
# Mini Project : Parameter Extractor

urls = [
    "https://site.com/profile?id=1",
    "https://site.com/search?q=test",
    "https://site.com/redirect?url=test"
]

params = set()

for url in urls:
    if "?" in url:
        query = url.split("?")[1]
        parameter = query.split("=")[0]
        params.add(parameter)

print(params)