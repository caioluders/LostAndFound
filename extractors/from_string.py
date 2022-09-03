import re, sys

def extract(txt) :
	grab_links = r"""://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+""" # needs improvement
	result = re.findall(grab_links,txt)
	return result

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py string.txt")
	txt = open(sys.argv[1],"r").read()

	print(extract(txt))

if __name__ == "__main__" :
	main()
