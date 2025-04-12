from browser_manager.manager import BrowserManager

if __name__ == '__main__':
    api_pre = 'http://43.160.195.19'
    chat_id = '6760644170'
    max_browser_num = 1
    browser_manager = BrowserManager(chat_id,api_pre,max_browser_num)
    browser_manager.init_browsers()
    browser_manager.run()