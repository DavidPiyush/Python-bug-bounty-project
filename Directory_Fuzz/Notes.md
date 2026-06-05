**Challenge: Build a Directory Fuzzer**

A directory fuzzer takes a URL and a wordlist, then checks which paths exist on a website.

```
Input:  https://example.com  +  wordlist.txt
Output: 
  [200] https://example.com/admin
  [200] https://example.com/login  
  [403] https://example.com/secret  ← exists but forbidden — interesting!
  [404] https://example.com/nothing ← skip these
```

**Your wordlist file (save as `wordlist.txt`):**

```markdwon
admin
login
dashboard
api
config
backup
test
dev
secret
uploads
```
