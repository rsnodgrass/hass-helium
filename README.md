# Helium Hotspot for Home Assistant

![beta_badge](https://img.shields.io/badge/maturity-Beta-yellow.png)
![release_badge](https://img.shields.io/github/release/rsnodgrass/hass-helium.svg)
![release_date](https://img.shields.io/github/release-date/rsnodgrass/hass-helium.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/DYks67r)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)  

Creates sensors to monitor Helium hotspots.

## Installation

Make sure [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) is installed, then add the repository: `rsnodgrass/hass-helium`

### Configuration

```yaml
sensor:
  - platform: helium
    hotspot_address:
```

NOTE: By default this updates the state from Helium Blockchain every 15 minutes. The check interval can be changed in yaml config by adding a 'scan_interval' for the sensor.

### Example Lovelace UI

```yaml
entities:
  - entity: sensor.helium_hotspot_name
type: entities
title: Helium
show_header_toggle: false
```
## Support

### Community Support

* Home Assistant Community Forums
* Helium Discord

### Feature Requests

* 

### See Also

* [Helium](https://helium.com/)
* Helium hotspot referer link
