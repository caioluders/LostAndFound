import subprocess, os, sys, shutil, tempfile, glob


def extract(apk):
	if not os.path.isfile(apk):
		sys.exit("[!] %s is not a file" % (apk))

	if not shutil.which("apktool") :
		sys.exit("[!] apktool not installed")

	temp_dir = tempfile.TemporaryDirectory().name

	apktool_cmd = subprocess.Popen(["apktool","d",apk,"-o",temp_dir], 
									stdout = subprocess.PIPE, 
									stderr=subprocess.PIPE)

	stdout, stderr = apktool_cmd.communicate()

	if stderr :
		sys.exit("[!] %s" % stderr)

	urls = set()

	for filename in glob.iglob(temp_dir+"/**/**",recursive=True) :
		if os.path.isfile(filename): 
			[ urls.add(u) for u in from_binary.extract(filename) ]

	print(stdout)

	return urls


def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] APK required; python3 from_apk.py folder/app.apk") 
	print(extract(sys.argv[1]))

if __name__ == '__main__':
	import from_binary
	main()
else :
	from . import from_binary