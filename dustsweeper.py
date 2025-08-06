import requests
from decimal import Decimal

# Поддерживаются сети через Blockchair API
SUPPORTED_NETWORKS = {
    "bitcoin": "https://api.blockchair.com/bitcoin/dashboards/address/",
    "litecoin": "https://api.blockchair.com/litecoin/dashboards/address/",
    "dogecoin": "https://api.blockchair.com/dogecoin/dashboards/address/"
}

DUST_THRESHOLDS = {
    "bitcoin": Decimal("0.00001"),
    "litecoin": Decimal("0.001"),
    "dogecoin": Decimal("1")
}

class DustSweeper:
    def __init__(self, network: str, addresses: list[str]):
        if network not in SUPPORTED_NETWORKS:
            raise ValueError(f"Network '{network}' not supported.")
        self.network = network
        self.api_base = SUPPORTED_NETWORKS[network]
        self.addresses = addresses

    def fetch_balance(self, address: str) -> Decimal:
        url = f"{self.api_base}{address}"
        r = requests.get(url)
        data = r.json()
        satoshis = data['data'][address]['address']['balance']
        return Decimal(satoshis) / Decimal(1e8)

    def find_dust(self) -> dict:
        dust_addresses = {}
        threshold = DUST_THRESHOLDS[self.network]
        for addr in self.addresses:
            try:
                balance = self.fetch_balance(addr)
                if balance < threshold and balance > 0:
                    dust_addresses[addr] = balance
            except Exception as e:
                print(f"Error fetching {addr}: {e}")
        return dust_addresses
