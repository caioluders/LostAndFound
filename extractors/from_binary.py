import re, sys, os

def extract(bin_file) :

	if not os.path.isfile(bin_file):
		sys.exit("[!] %s is not a file" % (bin_file))

	grab_links = re.compile( # yonked from mobsf
        (
            b'((?:https?://|s?ftps?://|'
            b'file://|www\d{0,3}[.])'
            b'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
        ))

	f = open(bin_file,"rb").read()



	result = re.findall(grab_links,f)
	return result

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py bin")

	print(extract(sys.argv[1]))

if __name__ == "__main__" :
	main()
