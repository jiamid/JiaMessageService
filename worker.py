from browser_manager.manager import BrowserManager

if __name__ == '__main__':
    api_pre = 'http://43.160.195.19'
    browser_manager = BrowserManager(api_pre)
    browser_manager.init_browsers()
    browser_manager.run()