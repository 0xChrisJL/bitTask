from .carv import Carv
from .coingecko import Coingecko
from .discord import Discord
from .wallet import Wallet
from .other import Other
from .twitter import Twitter
from .zetalabs import Zetalabs


class taskBase:
    driver = None

    def __init__(self, driver):
        self.wallet = Wallet(driver)
        self.carv = Carv(driver)
        self.zetalabs = Zetalabs(driver)
        self.coingecko = Coingecko(driver)
        self.discord = Discord(driver)
        self.twitter = Twitter(driver)
        self.other = Other(driver)
