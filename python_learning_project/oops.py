class Target: # class
    domain = 'example.com'

    def __init__(self,domain): # Constructor
        self.domain = domain


    def info(self):
        print(f"Target: {self.domain}")
target = Target("api.example.com") # object


print(target.domain)
target.info()

# Inheritance


# class Scanner:
#     def scan(self):
#         print("Scanning...")

# class XSSScanner(Scanner):
#     pass

# scanner = XSSScanner()
# scanner.scan()



# -----------------

class Logger:
    def log(self,message):
        print(message)


class Scanner:
    def __init__(self):
        self.logger = Logger()

scanner = Scanner()
scanner.logger.log("Started Scan")

# Mini Project
# -------------

class Endpoint:
    def __init__(self,url,status):
        self.url = url
        self.status = status

    def info(self):
        print(f"{self.url}" f" -> " f"{self.status}")


e1 = Endpoint("https:/example.com",200)
e2 = Endpoint("https:/example.com/admin",403)

e1.info()
e2.info()

# Challenge

class Vulnerability:
    def __init__(self,type,severity,endpoint):
        self.type = type
        self.severity = severity
        self.endpoint = endpoint

    def show(self):
        print(f"Type: {self.type}")
        print(f"Severity: {self.severity}")
        print(f"Endpoint: {self.endpoint}")

xss = Vulnerability("XSS","High","/search")    

xss.show()