import requests, urllib

base_domains = ["twitter.com"]
cache_domains = set()


def check(url):
	
	# third-party check , maybe implement a headless browser
	url = "https://tweettunnel.com/"+url.split("twitter.com/")[1].split("/")[0]


	if url not in cache_domains :
		cache_domains.add(url) 


		r = requests.get(url)

		if r.status_code == 200 and "Sorry, that page does not exist." in r.text :
			print("[!] Twitter unregistred username:", url)

