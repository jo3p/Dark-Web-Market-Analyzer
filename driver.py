from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def create_webdriver():
    class WebDriver:
        """
        Extends the chromedriver class to be used as context manager.
        """

        def __init__(self, driver):
            self.driver = driver

        def __enter__(self):
            return self.driver

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.driver.quit()

    firefox_profile = FirefoxProfile('/etc/tor')

    # set some privacy settings
    firefox_profile.set_preference("places.history.enabled", False)
    firefox_profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
    firefox_profile.set_preference("privacy.clearOnShutdown.passwords", True)
    firefox_profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
    firefox_profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
    firefox_profile.set_preference("signon.rememberSignons", False)
    firefox_profile.set_preference("network.cookie.lifetimePolicy", 2)
    firefox_profile.set_preference("network.dns.disablePrefetch", True)
    firefox_profile.set_preference("network.http.sendRefererHeader", 0)

    # set socks proxy
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.socks_version", 5)
    firefox_profile.set_preference("network.proxy.socks", '127.0.0.1')
    firefox_profile.set_preference("network.proxy.socks_port", 9050)
    firefox_profile.set_preference("network.proxy.socks_remote_dns", True)

    # if you're really hardcore about your security
    # js can be used to reveal your true i.p.
    firefox_profile.set_preference("javascript.enabled", False)

    # get a huge speed increase by not downloading images
    firefox_profile.set_preference("permissions.default.image", 2)

    return WebDriver(Firefox(firefox_profile=firefox_profile))
