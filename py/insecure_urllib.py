import urllib.request
url = input("Enter URL: ")
response = urllib.request.urlopen(url)
print(response.read())

