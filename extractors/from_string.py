import re, sys

def extract(txt) :
	grab_links = re.compile( # yonked from mobsf
        (
            r'((?:https?://|s?ftps?://|'
            r'file://|www\d{0,3}[.])'
            r'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
        )) # needs improvement
	result = re.findall(grab_links,txt)
	return result

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py string.txt")
	txt = open(sys.argv[1],"r").read()

	print(extract(txt))

if __name__ == "__main__" :
	main()
