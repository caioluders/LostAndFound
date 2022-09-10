import aiodns, asyncio, sys, tqdm, string

class AsyncResolver(object):
	def __init__(self):
		self.timeout = 0.1
		self.loop = asyncio.get_event_loop()
		self.resolver = aiodns.DNSResolver(timeout=self.timeout, loop=self.loop)
		self.resolver.nameservers = ['8.8.8.8']

	async def query(self, domain, type):
		return await self.resolver.query(domain, type)

	def query_A(self, domain):
		"""query DNS A records.
		ex: {'domain': 'www.google.com','type': 'A','data': [u'93.46.8.89']}}
		"""
		f = self.query(domain, 'A')
		result = self.loop.run_until_complete(f)
		data = list(map(lambda x: x.host, result))
		item = {"domain": domain, "type": "A", "data": data}
		return item

def clean_domain(dirty_domain):
	allowed_chars = string.ascii_letters + string.digits + "-."

	for i in range(len(dirty_domain)) :
		if dirty_domain[i] not in allowed_chars:
			i -= 1
			break

	return dirty_domain[:i+1]

def check(domains):
	domains = filter(None, domains)
	domains = set(domains)
	dns_resolver = AsyncResolver()

	for d in tqdm.tqdm(domains) :
		d = clean_domain(d)
		try :
			dns_resolver.query_A(d)
		except aiodns.error.DNSError as error :
			if error.args[0] == 4 :
				print("[!] % NOT REGISTRED", d)

def check_passive(domain):

	dns_resolver = AsyncResolver()

	try :
		dns_resolver.query_A(domain)
	except aiodns.error.DNSError as error :
		if error.args[0] == 4 :
			return False

	return True

def main():
	if len(sys.argv) < 2 :
		sys.exit("[!] domain list file missing; python domain.py domains.txt")
	domain_list = open(sys.argv[1],"r").read().split("\n")
	check(domain_list)

if __name__ == "__main__" :
	main()
