# chrome driver site https://sites.google.com/chromium.org/driver/?pli=1
# xattr -d com.apple.quarantine chromedriver 
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = Options()
options.add_experimental_option("detach", True) # allow the window to remain open
options.headless = False
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

# configure chrome browser to not load images and javascript
options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

PATH = '/Users/dalmas.otieno/Documents/youtube/fifa-world-cup-data-analysis/cromedriver'
driver = webdriver.Chrome(PATH, options=options)

URL = 'https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022/scores-fixtures?country=UG&wtw-filter=ALL'
print(driver.title)
driver.get(URL)
