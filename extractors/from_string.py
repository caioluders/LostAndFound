import re, sys

# Protocol-based URLs
_proto_re = re.compile(
	r'((?:https?://|s?ftps?://|file://|s3://|gs://|'
	r'www\d{0,3}[.])'
	r'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
)

# JSON escaped URLs: https:\/\/example.com\/path
_escaped_re = re.compile(
	r'(https?:\\/\\/[\w().=/;,#:@?&~*+!$%\'{}\\\-]+)'
)

# Trailing junk that's not part of the URL
_trailing_junk = re.compile(r'[).,;:!?\'"}>]+$')


def _clean_trailing(url):
	"""Strip trailing punctuation that's not part of the URL."""
	# Balance parentheses - don't strip ) if there's a matching ( in URL
	cleaned = _trailing_junk.sub('', url)
	if '(' in url and ')' not in cleaned and ')' in url:
		cleaned = cleaned + ')'
	return cleaned


def extract(txt) :
	results = set()

	for url in _proto_re.findall(txt):
		results.add(_clean_trailing(url))

	# JSON escaped slashes
	for url in _escaped_re.findall(txt):
		results.add(_clean_trailing(url.replace('\\/', '/')))

	return list(results)

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py string.txt")
	txt = open(sys.argv[1],"r").read()

	print(extract(txt))

if __name__ == "__main__" :
	main()
