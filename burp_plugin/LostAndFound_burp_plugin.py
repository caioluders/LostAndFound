import fnmatch
from urlparse import urlparse
from burp import IBurpExtender
from burp import IScannerCheck
from burp import IProxyListener
from burp import IScanIssue
from array import array
from java.io import PrintWriter
from java.io import OutputStream
from java.lang import Runnable
from javax.swing import SwingUtilities

GREP_STRING = "github.com"
GREP_STRING_BYTES = bytearray(GREP_STRING)
INJ_TEST = bytearray("|")
INJ_ERROR = "Unexpected pipe"
INJ_ERROR_BYTES = bytearray(INJ_ERROR)

class BurpExtender(IBurpExtender, IScannerCheck, IProxyListener):

	#
	# implement IBurpExtender
	#

	def registerExtenderCallbacks(self, callbacks):
		# keep a reference to our callbacks object
		self._callbacks = callbacks

		# obtain an extension helpers object
		self._helpers = callbacks.getHelpers()

		# set our extension name
		callbacks.setExtensionName("Lost and Found")

		self._stdout = PrintWriter(callbacks.getStdout(), True)
		self._stderr = callbacks.getStderr()

		# domains cache

		self._domains_cache = set()

		# load checkers 

		self.checkers = self.load_checkers()

		# register ourselves as a custom scanner check
		callbacks.registerScannerCheck(self)


	def load_checkers(self):
		checkers_folder = "./checkers"
		checkers = {}
		checkers_files = os.listdir(checkers_folder)

		for c in checkers_files:
			location = os.path.join(checkers_folder,c)

			if c[-3:] != '.py' or os.path.isfile(location) != True :
				continue

			p = __import__("checkers."+c[:-3])
			checkers[c[:-3]] = getattr(p, c[:-3])

		return checkers

	# helper method to search a response for occurrences of a literal match string
	# and return a list of start/end offsets

	def _get_matches(self, response, match):
		matches = []
		start = 0
		reslen = len(response)
		matchlen = len(match)
		while start < reslen:
			start = self._helpers.indexOf(response, match, True, start, reslen)
			if start == -1:
				break
			matches.append(array('i', [start, start + matchlen]))
			start += matchlen

		return matches

	def fnmatch_all(self, text, filters):
		for f in filters:
			if fnmatch.fnmatch(text, f) :
				return True	
	#
	# implement IScannerCheck
	#

	def doPassiveScan(self, baseRequestResponse):
		# look for matches of our passive check grep string

		request_info = baseRequestResponse.getHttpService()
		request_response = self._helpers.bytesToString(baseRequestResponse.getResponse())
		request_url =  self._helpers.analyzeRequest(baseRequestResponse).getUrl().toString()
		request_code = self._helpers.analyzeResponse(request_response).getStatusCode()

		matches = []

		for c in self.checkers :
			if hasattr(self.checkers[c], "base_domains") :

				if self.fnmatch_all(request_info.getHost(), self.checkers[c].base_domains) :
					if self.checkers[c].check( request_url, request_response, request_code ) :
						self._stdout.println("vulnerable "+request_url)
						matches.append(CustomScanIssue(
							baseRequestResponse.getHttpService(),
							self._helpers.analyzeRequest(baseRequestResponse).getUrl(),
							[self._callbacks.applyMarkers(baseRequestResponse, None, matches)],
							c+" Not Found",
							"The active was not found",
							"Information"))

		if (len(matches) == 0):
			return None

		# report the issue
		return matches

	def consolidateDuplicateIssues(self, existingIssue, newIssue):
		# This method is called when multiple issues are reported for the same URL 
		# path by the same extension-provided check. The value we return from this 
		# method determines how/whether Burp consolidates the multiple issues
		# to prevent duplication
		#
		# Since the issue name is sufficient to identify our issues as different,
		# if both issues have the same name, only report the existing issue
		# otherwise report both issues
		if existingIssue.getIssueName() == newIssue.getIssueName():
			return -1

		return 0

#
# class implementing IScanIssue to hold our custom scan issue details
#
class CustomScanIssue (IScanIssue):
	def __init__(self, httpService, url, httpMessages, name, detail, severity):
		self._httpService = httpService
		self._url = url
		self._httpMessages = httpMessages
		self._name = name
		self._detail = detail
		self._severity = severity

	def getUrl(self):
		return self._url

	def getIssueName(self):
		return self._name

	def getIssueType(self):
		return 0

	def getSeverity(self):
		return self._severity

	def getConfidence(self):
		return "Certain"

	def getIssueBackground(self):
		pass

	def getRemediationBackground(self):
		pass

	def getIssueDetail(self):
		return self._detail

	def getRemediationDetail(self):
		pass

	def getHttpMessages(self):
		return self._httpMessages

	def getHttpService(self):
		return self._httpService


class ScannerRunnable(Runnable):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)