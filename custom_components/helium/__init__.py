"""Integration with Helium"""

import asyncio

from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the Helium component."""
    return True