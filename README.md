# Simple Golink Server 

No-frills server for generating golinks in my LAN.

## Setup instructions

Run `python3 db.py` to generate the SQLite DB.

Then daemonize the flask app (see instructions [here](https://samliu.github.io/2022/04/26/golink-server.html)) and set up a DNS server and reverse proxy to make your LAN use it.
