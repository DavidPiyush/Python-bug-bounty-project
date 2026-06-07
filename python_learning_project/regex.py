# Regex = Pattern Matching
import re

# re.search()

text = "admin123"
result = re.search(r"admin",text)

if result:
    print(f"Founded")


# re.findall()

text = "admin1 admin2 admin3"
matches = re.findall(r"admin\d",text)
matches = re.findall(r"\d+","id=123")
matches = re.findall(r"\d*","id=123")
matches = re.findall(r"\d{1,4}","12345")
# print(matches) # list


# Group

url ="id=123"
pattern =re.findall(r"id=(\d+)",url)
# print(pattern)

# Find Emails

response ="example@gmail.com"
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
result = re.findall(pattern,response)
print(result)


# Find URLs
response = "http://test.com"
pattern = r"https?://[^\s\"']+"
result = re.findall(pattern,response)
print(result)


# Mini Project: Secret Scanner
# ------------------------------
response = """
AWS_KEY=AKIAIOSFODNN7EXAMPLE
email=admin@example.com
"""

email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",response)

aws_key = re.findall( r"AKIA[0-9A-Z]{16}",response)

print(email)
print(aws_key)


# Challenge
# -------------------

js_file = """
https://api.example.com/login
https://api.example.com/user
https://admin.example.com/dashboard
"""

url = re.findall(r"https?://[^\s\"']+",js_file)
print(url)