import requests, sys, re, aiohttp, asyncio

async def requests_async(domains) :

	async with aiohttp.ClientSession() as session:

			urls = []
			for d in domains :
				try:
					async with session.get(d) as resp :
						dc = await resp.text()
						print(d)
						[urls.append(u) for u in from_string.extract(dc)]
				except Exception as e:
					print("[!] Error %s " % str(e))

			return urls

def extract(domain):

	if type(domain) is list :
		urls = asyncio.run(requests_async(domain))

		return urls
		
	else :
		try :
			r = requests.get(domain, timeout=4)
			result = from_string.extract(r.text)
			return result
		except Exception as e :
			print("[!] Error %s " % e )
			return []

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] Url required; python3 from_url.py http://google.com") 
	print(extract(sys.argv[1]))

if __name__ == "__main__" :
	import from_string
	main()
else :
	from . import from_string
