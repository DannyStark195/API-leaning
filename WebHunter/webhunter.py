import requests
# web🕸hunter💻
# A mini web crawler
# Get's the html page of a web url
# Requires 'requests' module to be installed.
# type:pip install requests to install.
print("        web🕸hunter💻  ")
print("Get the html of any webpage")
website_name = input("Enter website name: ")

website_url = input("Enter website url: ")
if not website_url.startswith('http'):
    website_url = 'https://'+ website_url
webhunter = requests.get(website_url)
# print(webhunter.headers)
webfile = website_name + ".html"

if webhunter.status_code>=400:
    print(f'Error: {webhunter.status_code}')
else:
    with open(webfile, 'w') as file:
        file.write(webhunter.text)
        print(f"{webfile} saved")
