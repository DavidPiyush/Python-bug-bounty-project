# urls = [
#     "https://example.com/login",
#     "https://example.com/login",
#     "https://api.example.com/user",
#     "https://admin.example.com",
#     "https://api.example.com/user",
#     "https://example.com/register"
# ]



# reports ={
#     "total_urls":len(urls),
#     "unique_urls":len(set(urls)),
#     "urls":set(urls)
# }

# print(reports)


# Challenge upgrade 1

urls = [
    "https://api.example.com/user",
    "https://api.example.com/admin",
    "https://admin.example.com/login"
]

# reports={}

# for url in urls:
#     parts = url.split("/")
#     subdomain = parts[2]

#     if subdomain in reports:
#         reports[subdomain] +=1
#     else:
#         reports[subdomain] =1
    
    


# Challenge Upgrade 2

reports={
    "interesting":[]
}
keywords = ["login","admin","dashboard","api","register","upload"]

for url in urls:
    for key in keywords:
        if key in url:
            reports["interesting"].append(url)
            break

import json
# print(json.dumps(reports,indent=4))


# Challenge upgrade 3
urls = [
    "/search?q=<script>",
    "/api/user/1",
    "/index.php?id=1'--",
    "/profile?id=99"
]

findings = {
    "xss": [],
    "sqli": [],
    "idor": []
}

for url in urls:
    if "<script>" in url:
        findings['xss'].append(url)
    elif "'--" in url:
        findings["sqli"].append(url)
    elif "/api/user" in url or "/profile?id=" in url:
        findings["idor"].append(url)

print(json.dumps(findings,indent=4))