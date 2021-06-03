from homeassistant import config_entries
from .const import DOMAIN

import voluptuous as vol

#class HeliumConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
# async def async_step_user(self, info):
#        if info is not None:
#            pass  # TODO: process info
#
#        return self.async_show_form(
#            step_id="wallet", data_schema=vol.Schema({vol.Required("wallet_address"): str})
#        )
