def hello():
    print("hello")

x = hello

# x()

# Functions inside Functions

def outer():
    def inner():
        print("Inner")

    inner()

# outer()

# Returning functions

def outer():
    def inner():
        print("Scanning Running")
    return inner

scanner = outer()
# scanner()

# First decorator



def logger(func):
    def wrapper():
        print("Started")

        func()

        print("Finished")
    return wrapper

@logger
def scan():
    print("Scanning...")

# scans = logger(scan)

# scans()

# Passing Arguments

def logger(func):

    def wrapper(url):
        print("Scanning: ", url)

        func(url)

    return wrapper

# @logger
# def scan(url):
#     print(url)


# scan("https://example.com")


# better version
def log(func):
    def wrapper(*args,**kwargs):
        print(f"Running {func.__name__}")

        result = func(*args,**kwargs)

        print('finished')

        return result

    return wrapper

@log
def scan():
    print("Scanning")