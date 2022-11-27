import requests, urllib

base_domains = ["twitter.com"]
cache_domains = set()
deny_list_usernames = ["share"]

def check(url):
	
	if len(url.split("twitter.com/")) == 1 :
		return

	username = url.split("twitter.com/")[1].split("/")[0].split("?")[0]
	
	if username in deny_list_usernames :
		return

	# third-party check , maybe implement a headless browser
	url = "https://tweettunnel.com/"+username


	if url not in cache_domains :
		cache_domains.add(url) 


		r = requests.get(url)

		if r.status_code == 200 and "Sorry, that page does not exist." in r.text :
			print("[!] Twitter unregistred username:", url)

