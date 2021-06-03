# Helium Blockchain for Home Assistant

![Helium Logo](https://github.com/rsnodgrass/hass-helium/blob/master/img/logo@2x.png?raw=true)

![beta_badge](https://img.shields.io/badge/maturity-Beta-yellow.png)
![release_badge](https://img.shields.io/github/release/rsnodgrass/hass-helium.svg)
![release_date](https://img.shields.io/github/release-date/rsnodgrass/hass-helium.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/DYks67r)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)  

Sensors for monitoring individual [Helium hotspots](https://rakwireless.kckb.st/544e97e6), Helium blockchain wallets, and the Helium HNT/USD Oracle price.

## Installation

Make sure [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) is installed, then add the repository: `rsnodgrass/hass-helium`

### Configuration

The bare minimum configuration creates general sensors to track the Helium blockchange, notably the HNT/USD Oracle price.

```yaml
sensor:
  - platform: helium
```

Configure Helium hotspot sensors:

```yaml
sensor:
  - platform: helium
    hotspots:
      - 112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn
      - xx
```

Configure Helium wallet sensors:

```yaml
sensor:
  - platform: helium
    wallets:
      - 12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
      - 14YeKFGXE23yAdACj6hu5NWEcYzzKxptYbm5jHgzw9A1P1UQfMv
```

NOTE: By default, the sensors update from the Helium Blockchain every 15 minutes. This interval can be changed by adding a 'scan_interval' entry for the sensor.

### Example Lovelace UI

```yaml
entities:
  - entity: sensor.helium_hotspot_name
type: entities
title: Helium
show_header_toggle: false
```

## Support

This is a community supported custom component integration for Home Assistant. Code improvents and Pull Requests are appreciated.
### Community Support

* [Home Assistant Community Forums](https://community.home-assistant.io/c/projects/custom-components/47)
* [Helium Discord](https://discord.com/invite/helium)

### Feature Requests

* 

### See Also

* [Helium](https://helium.com/)
* [Order Helium hotspot from RAK Wireless](https://rakwireless.kckb.st/544e97e6)
