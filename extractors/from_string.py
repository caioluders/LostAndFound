import re, sys

def main(txt) :
	grab_links = re.compile("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
	result = re.findall(grab_links,txt)
	return result

if __name__ == "__main__" :
	if len(sys.argv) < 2 :
		sys.exit("[!] string file needed; python from_string.py string.txt")
	txt = open(sys.argv[1],"r").read()
	print(main(txt))
