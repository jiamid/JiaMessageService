from browser_manager.manager import BrowserManager

if __name__ == '__main__':
    api_pre = 'http://127.0.0.1:9998'
    browser_manager = BrowserManager(api_pre)
    browser_manager.init_browsers()
    browser_manager.run()