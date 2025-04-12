from browser_manager.manager import BrowserManager
from commonts.settings import settings

if __name__ == '__main__':
    api_pre = settings.worker_api_pre
    chat_id = settings.worker_chat_id
    max_browser_num = 1
    browser_manager = BrowserManager(chat_id,api_pre,max_browser_num)
    browser_manager.init_browsers()
    browser_manager.run()