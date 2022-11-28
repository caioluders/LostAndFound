import subprocess, os, sys, shutil, tempfile, glob

def extract(directory):
	if not os.path.isdir(directory):
		sys.exit("[!] %s is not a directory" % (directory))

	urls = set()

	for filename in glob.iglob(directory+"/**/**",recursive=True) :
		if os.path.isfile(filename): 
			[ urls.add(u) for u in from_binary.extract(filename) ]

	return urls


def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] DIR required; python3 from_dir.py folder/")
	print(extract(sys.argv[1]))

if __name__ == '__main__':
	import from_binary
	main()
else :
	from . import from_binary