import re, sys, os

# Protocol-based URLs
_proto_re = re.compile(
	b'((?:https?://|s?ftps?://|file://|s3://|gs://|'
	b'www\\d{0,3}[.])'
	b'[\\w().=/;,#:@?&~*+!$%\'{}-]+)'
)

# JSON escaped URLs
_escaped_re = re.compile(
	b'(https?:\\\\/\\\\/[\\w().=/;,#:@?&~*+!$%\'{}\\\\-]+)'
)

_trailing_junk = re.compile(b'[).,;:!?\'"}>]+$')


def _clean_trailing(url):
	cleaned = _trailing_junk.sub(b'', url)
	if b'(' in url and b')' not in cleaned and b')' in url:
		cleaned = cleaned + b')'
	return cleaned


def extract(bin_file) :

	if not os.path.isfile(bin_file):
		sys.exit("[!] %s is not a file" % (bin_file))

	f = open(bin_file,"rb").read()

	results = set()

	for url in _proto_re.findall(f):
		results.add(_clean_trailing(url))

	for url in _escaped_re.findall(f):
		results.add(_clean_trailing(url.replace(b'\\/', b'/')))

	return list(results)

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py bin")

	print(extract(sys.argv[1]))

if __name__ == "__main__" :
	main()
