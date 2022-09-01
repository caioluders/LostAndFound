import aiodns, asyncio, sys

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


def main(domains):
	dns_resolver = AsyncResolver()

	for d in domains :
		try :
			dns_resolver.query_A(d)
		except aiodns.error.DNSError as error :
			print("[!] % NOT REGISTRED", d)

if __name__ == "__main__" :
	if len(sys.argv) < 2 :
		sys.exit("[!] domain list file missing; python domain.py domains.txt")
	domain_list = open(sys.argv[1],"r").read().split("\n")
	main(domain_list)
