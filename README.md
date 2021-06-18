# Helium Blockchain for Home Assistant

![Helium Logo](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/logo@2x.png)

Sensors for monitoring individual [Helium hotspots](https://rakwireless.kckb.st/544e97e6), Helium blockchain wallets, and the Helium HNT/USD Oracle price.

![beta_badge](https://img.shields.io/badge/maturity-Beta-yellow.png)
![release_badge](https://img.shields.io/github/release/rsnodgrass/hass-helium.svg)
![release_date](https://img.shields.io/github/release-date/rsnodgrass/hass-helium.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/DYks67r)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)  

## Installation

Make sure [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) is installed. This integration is part of the default HACS store (though can also be added manually using repository: `rsnodgrass/hass-helium`)

### Configuration

The bare minimum configuration creates general sensors to track the Helium blockchange, notably the HNT/USD Oracle price.

```yaml
sensor:
  - platform: helium
```

Configure sensors for Helium hotspots:

```yaml
sensor:
  - platform: helium
    hotspots:
      - 112JbKk4fvYmoSqHR93vRYugjiduT1JrF8EyC86iMUWjUrmW95Mn
```

Configure sensors for Helium wallets:

```yaml
sensor:
  - platform: helium
    wallets:
      - 12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
      - 14YeKFGXE23yAdACj6hu5NWEcYzzKxptYbm5jHgzw9A1P1UQfMv
```

NOTE: By default, the sensors update from the Helium Blockchain every 15 minutes. This interval can be changed by adding a 'scan_interval' entry for the sensor, but this effects all sensors. You can create automations to dynamically trigger more frequent of specific sensors using the '[homeassistant.update_entity](https://www.home-assistant.io/integrations/homeassistant/#service-homeassistantupdate_entity)' service call.

### Advanced Configuration

This configuration.yaml setting adds a sensor to track total HNT added to wallet by day/week/month usng the [utility meter](https://www.home-assistant.io/integrations/utility_meter/) integration.

```yaml
utility_meter:
  helium_wallet_today:
    source: sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
    cycle: daily

  helium_wallet_weekly:
    source: sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
    cycle: weekly

  helium_wallet_monthly:
    source: sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
    cycle: monthly
```

### Example Lovelace UI

Status of Helium hotspots using [uptime card](https://github.com/dylandoamaral/uptime-card):

![Lovelace Status Example](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/lovelace-hotspot-status.png)


```yaml
type: custom:uptime-card
entity: sensor.helium_rough_chili_bird
icon: mdi:router-wireless
ok: online
ko: offline
ko_icon: mdi:router-wireless-off
hours_to_show: 24
status_adaptive_color: true
color:
  icon: grey
show:
  icon: true
  status: false
  timeline: true
  average: true
title_adaptive_color: true
name: Rough Chili Bird
```


#### HNT Price Tracking

Track the price of HNT using mini-graph-card:

![Lovelace Price Example](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/lovelace-price.png)

```yaml
animate: true
entities:
  - entity: sensor.helium_hnt_oracle_price
    name: HNT/USD
graph: line
hour24: true
font_size: 75
hours_to_show: 24
points_per_hour: 12
name: Helium HNT/USD
show:
  extrema: true
  icon: false
  name: true
type: custom:mini-graph-card
```

![Lovelace Price Example](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/lovelace-price-2.png)

Track the price of HNT using apexchart-card:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Helium HNT/USD
  show_states: true
  colorize_states: true
series:
  - entity: sensor.helium_hnt_oracle_price
  - entity: sensor.helium_hnt_oracle_price
    type: column

```

For custom price alerts ideas, see [example stock alert](https://blog.kevineifinger.de/archive/2019/10/17/Using-Homeassistant-As-My-Self-Hosted-Stock-Alert.html).

#### Helium Wallet

Helium wallet size per day over last 7 days:

```yaml
entities:
  - entity: sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U
    name: Wallet HNT
hours_to_show: 168
icon: mdi:cash
name: Helium Wallet
group_by: date
show:
  graph: bar
  icon: false
  state: true
type: custom:mini-graph-card
```

Wallet value:

```yaml
  - platform: template
    sensors:
      helium_wallet_value:
        value_template:
          "{{ sensor.helium_hnt_oracle_price * sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U }}"  
```

#### Total HNT Mined Today

This requires the advanced configuration above to add a utility meter for tracking today's HNT wallet amount versus yesterday's wallet. This requires the `[apexcharts-card](https://github.com/RomRider/apexcharts-card)` is installed.


![Lovelace Today Example](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/lovelace-mined-today.png)

```yaml
type: custom:config-template-card
entities:
  - sensor.helium_wallet_today
card:
  type: custom:apexcharts-card
  header:
    show: true
    show_states: true
    colorize_states: true
    title: Helium Mined Today
  span:
    start: day
  graph_span: 24h
  all_series_config:
    stroke_width: 4
    type: line
    extend_to_end: false
    float_precision: 2
  color_list:
    - lightblue
    - grey
  series:
    - entity: sensor.helium_wallet_today
      name: Today
      type: area
      group_by:
        func: avg
        duration: 20min
    - entity: sensor.helium_wallet_today
      name: Yesterday
      offset: '-24h'
      opacity: 0.2
      group_by:
        func: avg
        duration: 20min
      show:
        in_header: true
  y_axis_precision: 0
  apex_config:
    yaxis:
      - seriesName: HNT
        decimalsInFloat: 0
      - seriesName: Helium
        show: false
    tooltip:
      x:
        format: ddd dd MMM - HH:mm
    xaxis:
      tooltip:
        enabled: false
    legend:
      show: false
    grid:
      borderColor: '#7B7B7B'
    chart:
      foreColor: '#7B7B7B'
      toolbar:
        show: false
```

## Support

This is a community supported custom component integration for Home Assistant. Code improvents and Pull Requests are appreciated.

#### Community Support

* [Home Assistant Community Forums](https://community.home-assistant.io/c/projects/custom-components/47)
* [Helium Discord](https://discord.com/invite/helium)

#### Feature Requests

* allow auto-creating sensors for ALL hotspots for a given wallet (optionally) 
* create sensor for current wallet value (based on Oracle HNT price)
* create sensors or attributes for being able to display per-hotspot rewards per 24-hour, 7-day, 30-day
* disable polling to allow dynamic scan intervals (e.g. every min for price, every 15 min for hotspot avail, every hour for wallet value)

## See Also

* [Helium](https://helium.com/)
* [Order Helium hotspot from RAK Wireless](https://rakwireless.kckb.st/544e97e6)
* [Koinly tax reporting](https://koinly.io?via=5CB65BB1) (supports Helium)
