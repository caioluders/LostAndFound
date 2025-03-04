import requests, urllib

base_domains = ["youtube.com"]
cache_domains = set()
deny_list_usernames = ["share","intent"]

def check(url):
	
	if len(url.split("youtube.com/")) == 1 :
		return

	try :
		username = url.split("youtube.com/@")[1].split("/")[0].split("?")[0]
	except :
		return

	if username in deny_list_usernames :
		return

	# third-party check , maybe implement a headless browser
	url = "https://socialblade.com/youtube/user/"+username


	if url not in cache_domains :
		cache_domains.add(url) 


		r = requests.get(url)

		if r.status_code == 200 and "Uh Oh! It seems that" in r.text :
			print("[!] Youtube unregistred username:", url)

