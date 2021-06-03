
import asyncio
import logging
import re

import httpx
from bs4 import BeautifulSoup

from .const import DEFAULT_TIMEOUT

LOG = logging.getLogger(__name__)

# see https://documenter.getpostman.com/view/8776393/SVmsTzP6?version=latest
WALLET_URL = 'https://api.helium.io/v1/accounts/'
HOTSPOT_URL = 'https://api.helium.io/v1/hotspots/'
NETWORK_STATS_URL = 'https://explorer.helium.foundation/api/stats'
ORACLE_PRICE_URL = 'https://api.helium.io/v1/oracle/prices/current'
HOTSPOTS_FOR_WALLET_URL = 'https://api.helium.io/v1/accounts/{address}/hotspots'

class SimpleHeliumClient:
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self._timeout = timeout

        self._wallets = []
        self._hotspots = []

    async def async_get(self, url):
        """Fetch JSON data from URL"""
        async with httpx.AsyncClient() as client:
            LOG.info(f"GET {url}")
            response = await client.request('GET', url, timeout=self._timeout)
            LOG.debug(f"GET {url} response: {response.status_code}")

            if response.status_code == httpx.codes.OK:
                return response.json()

        return None

    async def async_get_hotspot_data(self, address):
        url = HOTSPOT_URL + address
        return await self.async_get(url)

    async def async_get_wallet_data(self, address):
        url = WALLET_URL + address
        return await self.async_get(url)

    async def async_get_wallet_hotspots(self, wallet_address):
        url = f"https://api.helium.io/v1/accounts/{wallet_address}/hotspots"
        return await self.async_get(url)

    async def async_get_oracle_price(self):
        url = ORACLE_PRICE_URL
        return await self.async_get(url)

    async def async_get_network_stats(self):
        url = NETWORK_STATS_URL
        return await self.async_get(url)
