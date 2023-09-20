#-*-coding: utf-8-*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager
import flask
import traceback, os, time

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

ADMIN_ID = "admin"
ADMIN_PASS = os.getenv("admin_password")

server1_challs = {
	"xss1": "9001",
	"xss2": "9002",
	"xss3": "9003",
	"csrf1": "9004",
	"csrf2": "9005",
	"xsleak": "9006",
}

def interceptor(request):
	pass

class Crawler:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('--no-sandbox')
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option("useAutomationExtension", False)

		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		self.driver.request_interceptor = interceptor
		self.driver.implicitly_wait(3)
		self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'navigator.'})
		self.driver.set_page_load_timeout(3)

	def req(self, url):
		try:
			print(f"[+] doing crawler req {url}")
			self.driver.get(url)
		except:
			print(f"[x] crawler driver req fail - {url}")
			print(traceback.format_exc())
			return False

		return self.driver

def doCrawl_server1(chal, url):
	crawler = Crawler()
	driver = crawler.driver
	try:
		crawler.req(f'http://arang_client:{server1_challs[chal]}/login')

		driver.find_element(By.ID,"userid").send_keys(ADMIN_ID)
		driver.find_element(By.ID,"userpw").send_keys(ADMIN_PASS)
		driver.find_element(By.ID,"submit-login").click()
		
		time.sleep(1)

		if crawler.req(url):
			time.sleep(2)
		
		driver.quit()
	except:
		driver.quit()
		print(f"[x] error...")
		print(traceback.format_exc())

def doCrawl_server2(url):
	crawler = Crawler()
	driver = crawler.driver
	try:
		if crawler.req(url):
			time.sleep(10)
		
		driver.quit()
	except:
		driver.quit()
		print(f"[x] error...")
		print(traceback.format_exc())


@app.route("/run", methods=["POST"])
def run():
	url = flask.request.form['url']
	if 'chal' in flask.request.form:
		chal = flask.request.form['chal']
		print(f"[+] bot run arang_client:{chal} - {url}")
		doCrawl_server1(chal, url)
	else:
		print(url)
		doCrawl_server2(url)

	return "<script>history.go(-1);</script>"
		

if __name__ == "__main__":
	try:
		app.run(host="0.0.0.0", port=9000, debug=True)
	except Exception as ex:
		logging.info(str(ex))
		pass