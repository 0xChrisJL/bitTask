import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from taskCode.actions import Config
from taskCode.task import taskBase

s = requests.session()
url = "http://127.0.0.1:54200"


# 打开比特浏览器
def bit_openBrowser(Id):
    headers = {'id': Id, 'loadExtensions': True}
    a = s.post(f"{url}/browser/open", json=headers).json()
    return a['data']['http']


# 关闭比特浏览器
def bit_stopBrowser(Id):
    headers = {'id': Id, }
    s.post(f"{url}/browser/close", json=headers).json()


# 初始化比特浏览器
def browser(Id):
    chrome_driver = "D:\\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", bit_openBrowser(Id))
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    return driver


if __name__ == "__main__":
    all_bitNum = Config.all_bit()
    for x in range(1, len(all_bitNum)+1):
        # 定义acc为账号id
        bitId = Config.bitId(x)
        # 定义adsNUm为窗口编号
        bitNum = Config.bitNum(x)
        # 定义adsAddress为钱包地址
        bitAddress = Config.bitAddress(x)
        # 定义password为密码
        password = Config.password()
        # 初始化比特的浏览器
        tb = taskBase(browser(bitId))

        # 执行任务
        try:
            tb.other.gamma_x(x)
        except BaseException:
            pass
        # 关闭浏览器
        bit_stopBrowser(bitId)
