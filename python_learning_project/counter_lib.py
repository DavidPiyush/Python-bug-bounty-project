from collections import Counter
from collections import defaultdict
from collections import deque
from collections import namedtuple


# Without Counter
subdomains = [
    "api.example.com",
    "api.example.com",
    "admin.example.com"
]

counts = {}

for subdomain in subdomains:

    if subdomain in counts:
        counts[subdomain] += 1
    else:
        counts[subdomain] = 1

print(counts)

# With Counter

result = Counter(subdomains)
print(result)
print(result.most_common())


params = ["id","id","q","redirect","id"]

query = Counter(params)
print(query.most_common())

# defaultdict

findings = defaultdict(list)

findings["xss"].append('/search')
findings["xss"].append('/profile')

print(findings)

urls = [
    ("200", "/"),
    ("200", "/login"),
    ("404", "/admin")
]

grouped = defaultdict(list)

for status,url in urls:
    grouped[status].append(url)

print(grouped)

# Mini Project

urls = [
    "/login",
    "/login",
    "/login",
    "/admin",
    "/admin",
    "/profile"
]

url_list = Counter(urls)
print(url_list)

findings = defaultdict(list)

findings["xss"].append('/search')
findings["idor"].append('/api/user/1')

print(findings)

# Queue

queue = deque()

queue.append("https://site.com")
queue.append("https://site.com")
queue.append("https://site.com")
queue.append("https://site.com")

while queue:
    current = queue.popleft()
    print(current)


# Named tuple

Endpoint = namedtuple("Endpoint",["url",'status','length'])
endpoint = Endpoint('/adim',403,523)

print(endpoint.status)