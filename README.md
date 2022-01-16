# Helium Blockchain for Home Assistant

![Helium Logo](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/logo@2x.png)

Sensors for monitoring individual [Helium hotspots](https://rakwireless.kckb.st/544e97e6), Helium blockchain wallets, and the Helium HNT/USD Oracle price for [Home Assistant](https://www.home-assistant.io/). For more detailed metrics, [HeliumTracker](https://heliumtracker.io/invite/5119) gives more detailed analytics over time including dashboards for your hosts.

![beta_badge](https://img.shields.io/badge/maturity-Beta-yellow.png)
![release_badge](https://img.shields.io/github/release/rsnodgrass/hass-helium.svg)
![release_date](https://img.shields.io/github/release-date/rsnodgrass/hass-helium.svg)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://buymeacoffee.com/DYks67r)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)  

Support this project, sign up for a [Crypto.com account as one of your HNT exchanges](https://platinum.crypto.com/r/a8xydwpxxj) and use referral code `a8xydwpxxj` to get a free $25 credit.

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

Track the price of HNT using [apexcharts-card](https://github.com/RomRider/apexcharts-card):

![Lovelace Price Example](https://raw.githubusercontent.com/rsnodgrass/hass-helium/main/img/lovelace-price-2.png)

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
          "{{ (states('sensor.helium_hnt_oracle_price') |float(0) * states('sensor.helium_wallet_12ywrqqzeNFwSMvCcaohpVdiwEeK4NZChtL9rs7dhKYd85fKG9U') | float(0)) | round(2) }}"  
```

#### Total HNT Mined Today

This requires the advanced configuration above to add a utility meter for tracking today's HNT wallet amount versus yesterday's wallet. This requires the [apexcharts-card](https://github.com/RomRider/apexcharts-card).


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

## Is there a way to change fiat currency from USD to EUR, GBP, CAD, etc?

No. **By design, Helium HNT is currently tightly coupled with USD since both the Oracles are all in USD and the Helium DC (Data Credits) are all fixed to USD prices.** However, you can of course convert from the USD price to other currencies using add on sensors.

For example, setting up conversion to CAD:

```yaml
sensor:
  - platform: openexchangerates
    name: Canadian Currency
    api_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    quote: CAD

  - platform: template
      sensors:
        helium_wallet_value:
          entity_id: sensor.helium_wallet_xxxxxxxxxxxxx, sensor.helium_hnt_oracle_price
          value_template: "{{ ((states('sensor.helium_hnt_oracle_price') | float(0)  * states('sensor.helium_wallet_xxxxxxxx') | float(0)) * states('sensor.canadian_currency') | float(0)) | round(2) }}"
          unit_of_measurement: "CAD"
```

And a simple Lovelace display (thanks @ThaNerd):

```yaml
- type: custom:apexcharts-card
  header:
    show: true
    title: Helium Wallet/CAD
    show_states: true
    colorize_states: true
  series:
    - entity: sensor.helium_wallet_value
      name: Helium Wallet
      type: column
```

## Support

This is a [community supported](https://community.home-assistant.io/t/helium-blockchain-custom-component/312984) custom component integration for Home Assistant. Code improvents and Pull Requests are appreciated.

#### Community Support

* [Home Assistant Community Forums](https://community.home-assistant.io/t/helium-blockchain-custom-component/312984)
* [Helium Discord](https://discord.com/invite/helium)

#### Feature Requests

* allow auto-creating sensors for ALL hotspots for a given wallet (optionally) 
* create sensor for current wallet value (based on Oracle HNT price)
* create sensors or attributes for being able to display per-hotspot rewards per 24-hour, 7-day, 30-day
* disable polling to allow dynamic scan intervals (e.g. every min for price, every 15 min for hotspot avail, every hour for wallet value)

#### Out of Scope

* local access to Helium hotspot status from proprietary vendor APIs (e.g. [Bobcat diagnosis interface](https://jamesachambers.com/bobcat-300-diagnoser-tool-utility-guide-helium-mining/)) -- love this idea, but this should be a separate Home Assistant integration

Here is an example for Bobcat 300's using the [RESTful sensor](https://www.home-assistant.io/integrations/rest/):

```yaml
sensor:
  - platform: rest
    name: "Bobcat Helium Sync Status"
    scan_interval: 300 # 5 min
    resource: http://<your-bobcat-lan-ip>/status.json
    value_template: "{{ (value_json.miner_height|float / value_json.blockchain_height|float) | round(2) }}"
    unit_of_measurement: '%'
    json_attributes:
       - "status"
       - "miner_height"
       - "blockchain_height"
       - "gap"
       - "epoch"

  - platform: rest
    name: "Bobcat Temp 0"
    scan_interval: 305 # 5 min + 5 seconds
    resource: http://<your-bobcat-lan-ip>/temp.json
    device_class: temperature
    value_template: "{{value_json.temp0|float}}"
    unit_of_measurement: "°C"

  - platform: rest
    name: "Bobcat Temp 1"
    scan_interval: 310 # 5 min + 10 seconds
    resource: http://<your-bobcat-lan-ip>/temp.json
    device_class: temperature
    value_template: "{{value_json.temp1|float}}"
    unit_of_measurement: "°C"

  - platform: rest
    name: "Bobcat Light"
    scan_interval: 300 # 5 min
    resource: http://<your-bobcat-lan-ip>/led.json
    value_template: "{{value_json.led}}"
    unit_of_measurement: "color"
```
Note: If you make multiple calls on bobcat API, make sure that you make unsynchronized calls in order to avoid the bobcat API error 'rate limit exceeded'.

## See Also

* [Helium antennas and accessories (US)](https://fiz-tech.net/collections/all?ref=shark)
* [HeliumTracker](https://www.heliumtracker.io/invite/5119) - excellent hotspot tracker
* [Order Helium hotspot from RAK Wireless](https://rakwireless.kckb.st/544e97e6)
* [Koinly tax reporting](https://koinly.io?via=5CB65BB1) (supports Helium)
* [Crypto.com - get $25 free for opening account](https://platinum.crypto.com/r/a8xydwpxxj) - use referral code `a8xydwpxxj`
