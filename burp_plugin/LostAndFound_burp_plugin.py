import fnmatch
import imp
import inspect
import os
import re
import sys
import threading
from urlparse import urlparse

from burp import IBurpExtender
from burp import IScannerCheck
from burp import IScanIssue
from burp import ITab

from java.awt import BorderLayout, GridLayout, FlowLayout, Font, Color, Dimension
from java.net import URL
from javax.swing import (
    JPanel, JLabel, JCheckBox, JRadioButton, ButtonGroup,
    JScrollPane, JTextArea, JSplitPane, BorderFactory, BoxLayout,
    Box, SwingUtilities
)


# URL extraction regex (same as extractors/from_string.py, Python 2 compatible)
URL_PATTERN = re.compile(
    r'((?:https?://|s?ftps?://|file://|s3://|gs://|'
    r'www\d{0,3}[.])'
    r'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
)
TRAILING_JUNK = re.compile(r'[).,;:!?\'"}>]+$')


def clean_extracted_url(url):
    cleaned = TRAILING_JUNK.sub('', url)
    if '(' in url and ')' not in cleaned and ')' in url:
        cleaned = cleaned + ')'
    return cleaned


def extract_urls(text):
    urls = set()
    for url in URL_PATTERN.findall(text):
        urls.add(clean_extracted_url(url))
    return urls


class BurpExtender(IBurpExtender, IScannerCheck, ITab):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("Lost and Found")

        self._stdout = callbacks.getStdout()
        self._stderr = callbacks.getStderr()

        # Caches
        self._checked_urls = set()
        self._lock = threading.Lock()

        # Load checkers
        self.checkers = self._load_checkers()

        # Settings
        self._active_mode = False
        self._enabled_checkers = {}
        for name in self.checkers:
            self._enabled_checkers[name] = True

        # Build UI
        self._build_ui()

        # Register
        callbacks.registerScannerCheck(self)
        callbacks.addSuiteTab(self)

        self._log("[*] Lost and Found loaded - %d checkers available" % len(self.checkers))

    # ---- Checker Loading ----

    def _load_checkers(self):
        checkers = {}
        stderr = self._callbacks.getStderr()

        # Find the plugin file path. Jython doesn't set __file__.
        plugin_path = None

        # Try inspect on the class source file
        try:
            plugin_path = os.path.abspath(inspect.getfile(type(self)))
        except (TypeError, AttributeError):
            pass

        # Fallback: check if Burp gave us the filename via the extension
        if not plugin_path:
            try:
                plugin_path = os.path.abspath(
                    self._callbacks.getExtensionFilename()
                )
            except:
                pass

        if not plugin_path:
            stderr.write("[!] Cannot determine plugin path\n")
            return checkers

        checkers_folder = os.path.join(os.path.dirname(plugin_path), "checkers")
        stderr.write("[*] Looking for checkers in: %s\n" % checkers_folder)

        if not os.path.isdir(checkers_folder):
            stderr.write("[!] Checkers folder not found\n")
            return checkers

        # Add checkers folder to sys.path so imports within checkers work
        if checkers_folder not in sys.path:
            sys.path.insert(0, checkers_folder)

        for filename in sorted(os.listdir(checkers_folder)):
            if not filename.endswith('.py') or filename.startswith('_'):
                continue

            name = filename[:-3]
            filepath = os.path.join(checkers_folder, filename)
            try:
                # Use execfile to load the checker into a fresh namespace
                ns = {"__builtins__": __builtins__}
                execfile(filepath, ns)
                if 'base_domains' in ns and 'check' in ns:
                    # Wrap namespace as a simple object
                    checker = type('Checker', (), ns)
                    checkers[name] = checker
                    stderr.write("[*] Loaded checker: %s\n" % name)
                else:
                    stderr.write("[!] Checker %s missing base_domains or check\n" % name)
            except Exception as e:
                stderr.write("[!] Failed to load checker %s: %s\n" % (name, str(e)))

        return checkers

    # ---- UI ----

    def _build_ui(self):
        self._panel = JPanel(BorderLayout())

        # -- Top: Title --
        title_panel = JPanel(FlowLayout(FlowLayout.LEFT))
        title = JLabel("Lost and Found")
        title.setFont(Font("Dialog", Font.BOLD, 16))
        title_panel.add(title)
        version = JLabel("  v2.0")
        version.setForeground(Color.GRAY)
        title_panel.add(version)

        # -- Middle: Settings --
        settings_panel = JPanel()
        settings_panel.setLayout(BoxLayout(settings_panel, BoxLayout.Y_AXIS))
        settings_panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10))

        # Scanning mode
        mode_panel = JPanel()
        mode_panel.setLayout(BoxLayout(mode_panel, BoxLayout.Y_AXIS))
        mode_panel.setBorder(BorderFactory.createTitledBorder("Scanning Mode"))

        self._radio_passive = JRadioButton("Passive only - check URLs as Burp sees them", True)
        self._radio_active = JRadioButton("Passive + Active - also extract & check URLs from response bodies")

        self._radio_passive.addActionListener(lambda e: self._set_active_mode(False))
        self._radio_active.addActionListener(lambda e: self._set_active_mode(True))

        group = ButtonGroup()
        group.add(self._radio_passive)
        group.add(self._radio_active)

        mode_panel.add(self._radio_passive)
        mode_panel.add(Box.createRigidArea(Dimension(0, 5)))
        mode_panel.add(self._radio_active)
        settings_panel.add(mode_panel)

        settings_panel.add(Box.createRigidArea(Dimension(0, 10)))

        # Checker toggles
        checkers_panel = JPanel()
        checkers_panel.setBorder(BorderFactory.createTitledBorder("Enabled Checkers"))
        # 2 columns grid
        num_checkers = len(self.checkers)
        rows = (num_checkers + 1) // 2
        checkers_panel.setLayout(GridLayout(rows, 2, 10, 5))

        self._checker_checkboxes = {}
        for name in sorted(self.checkers.keys()):
            checker = self.checkers[name]
            display = getattr(checker, 'name', name)
            cb = JCheckBox(display, True)
            cb.addActionListener(lambda e, n=name: self._toggle_checker(n, e))
            self._checker_checkboxes[name] = cb
            checkers_panel.add(cb)

        settings_panel.add(checkers_panel)

        # -- Bottom: Log --
        self._log_area = JTextArea()
        self._log_area.setEditable(False)
        self._log_area.setFont(Font("Monospaced", Font.PLAIN, 12))
        self._log_area.setRows(10)
        log_scroll = JScrollPane(self._log_area)
        log_scroll.setBorder(BorderFactory.createTitledBorder("Activity Log"))

        # Assemble
        top_panel = JPanel(BorderLayout())
        top_panel.add(title_panel, BorderLayout.NORTH)
        top_panel.add(settings_panel, BorderLayout.CENTER)

        split = JSplitPane(JSplitPane.VERTICAL_SPLIT, top_panel, log_scroll)
        split.setResizeWeight(0.6)

        self._panel.add(split, BorderLayout.CENTER)

    def _set_active_mode(self, enabled):
        self._active_mode = enabled
        mode = "Passive + Active" if enabled else "Passive only"
        self._log("[*] Scanning mode: %s" % mode)

    def _toggle_checker(self, name, event):
        self._enabled_checkers[name] = event.getSource().isSelected()
        state = "enabled" if self._enabled_checkers[name] else "disabled"
        self._log("[*] Checker %s: %s" % (name, state))

    def _log(self, msg):
        def _append():
            self._log_area.append(msg + "\n")
            self._log_area.setCaretPosition(self._log_area.getDocument().getLength())
        SwingUtilities.invokeLater(_append)

    # ---- ITab ----

    def getTabCaption(self):
        return "Lost and Found"

    def getUiComponent(self):
        return self._panel

    # ---- IScannerCheck ----

    def _fnmatch_all(self, text, patterns):
        for p in patterns:
            if fnmatch.fnmatch(text, p):
                return True
        return False

    def _check_url(self, checker_name, checker, url, body, status_code, base_request_response):
        """Run a single checker against a URL. Returns CustomScanIssue or None."""
        with self._lock:
            cache_key = "%s:%s" % (checker_name, url)
            if cache_key in self._checked_urls:
                return None
            self._checked_urls.add(cache_key)

        result = checker.check(url, body, status_code)
        if result is None:
            return None

        detail = result.get("detail", "Broken asset detected")
        checker_display = getattr(checker, 'name', checker_name)
        sev = getattr(checker, 'severity', 'Medium')

        issue_name = "Lost&Found: %s" % checker_display
        issue_detail = (
            "<b>Checker:</b> %s<br>"
            "<b>URL:</b> %s<br>"
            "<b>Detail:</b> %s<br>"
        ) % (checker_display, url, detail)

        self._log("[!] FOUND - %s: %s" % (checker_display, detail))

        try:
            issue_url = URL(url)
        except:
            issue_url = self._helpers.analyzeRequest(base_request_response).getUrl()

        return CustomScanIssue(
            base_request_response.getHttpService(),
            issue_url,
            [base_request_response],
            issue_name,
            issue_detail,
            sev
        )

    def doPassiveScan(self, baseRequestResponse):
        response_bytes = baseRequestResponse.getResponse()
        if response_bytes is None:
            return None

        request_url = self._helpers.analyzeRequest(baseRequestResponse).getUrl().toString()
        parsed = urlparse(request_url)
        host = parsed.hostname or ""
        response_body = self._helpers.bytesToString(response_bytes)
        response_info = self._helpers.analyzeResponse(response_bytes)
        status_code = response_info.getStatusCode()

        issues = []

        # 1. Passive: check the request URL against matching checkers
        for name, checker in self.checkers.items():
            if not self._enabled_checkers.get(name, True):
                continue
            if not hasattr(checker, 'base_domains'):
                continue
            if self._fnmatch_all(host, checker.base_domains):
                issue = self._check_url(name, checker, request_url, response_body, status_code, baseRequestResponse)
                if issue:
                    issues.append(issue)

        # 2. Active: extract URLs from response body and check them
        if self._active_mode:
            extracted = extract_urls(response_body)
            for url in extracted:
                ext_parsed = urlparse(url)
                ext_host = ext_parsed.hostname or ""
                for name, checker in self.checkers.items():
                    if not self._enabled_checkers.get(name, True):
                        continue
                    if not hasattr(checker, 'base_domains'):
                        continue
                    if self._fnmatch_all(ext_host, checker.base_domains):
                        # Make an active request via Burp
                        try:
                            port = ext_parsed.port or (443 if ext_parsed.scheme == 'https' else 80)
                            use_https = ext_parsed.scheme == 'https'
                            http_service = self._helpers.buildHttpService(ext_host, port, use_https)
                            request = self._helpers.buildHttpRequest(URL(url))
                            active_response = self._callbacks.makeHttpRequest(http_service, request)

                            if active_response.getResponse() is not None:
                                active_body = self._helpers.bytesToString(active_response.getResponse())
                                active_info = self._helpers.analyzeResponse(active_response.getResponse())
                                active_status = active_info.getStatusCode()
                                issue = self._check_url(name, checker, url, active_body, active_status, active_response)
                                if issue:
                                    issues.append(issue)
                        except Exception as e:
                            pass

        return issues if issues else None

    def consolidateDuplicateIssues(self, existingIssue, newIssue):
        if existingIssue.getIssueName() == newIssue.getIssueName():
            if existingIssue.getIssueDetail() == newIssue.getIssueDetail():
                return -1
        return 0


class CustomScanIssue(IScanIssue):
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
        return (
            "Lost &amp; Found detects broken, expired, and unclaimed assets "
            "referenced in web applications. These can lead to subdomain takeover, "
            "dependency confusion, or account impersonation attacks."
        )

    def getRemediationBackground(self):
        return "Claim or remove references to the unclaimed resource."

    def getIssueDetail(self):
        return self._detail

    def getRemediationDetail(self):
        return None

    def getHttpMessages(self):
        return self._httpMessages

    def getHttpService(self):
        return self._httpService
