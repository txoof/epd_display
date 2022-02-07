## Additional Plugin Information
This plugin can track multiple crypto currencies by adding multiple entries in the configuration file:

```
[Plugin: Crypto Dogecoin v EUR]
plugin = crypto
layout = layout
# fiat currency to use for comparison
fiat = eur
# crypto currency to track
coin = dogecoin
# days of data to display
days = 14
# interval to show on sparkline
interval = hourly
# rss news feed to display
rss_feed = https://bitcoinmagazine.com/.rss/full/
min_display_time = 60
refresh_rate = 240
max_priority = 2

[Plugin: Crypto Bitcoin v USD]
plugin = crypto
layout = layout
# fiat currency to use for comparison
fiat = usd
# crypto currency to track
coin = bitcoin
# days of data to display
days = 14
# interval to show on sparkline
interval = hourly
# rss news feed to display
rss_feed = https://http://feeds.bbci.co.uk/news/world/rss.xml
min_display_time = 60
refresh_rate = 240
max_priority = 2

```