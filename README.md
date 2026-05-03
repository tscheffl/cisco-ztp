# Cisco-Lab ZTP

In diesem Projekt wird eine Lösung für einfaches Zero-Touch-Provisioning von Cisco Routern entwickelt. 

* Python **Flask** Webserver
* **dnsmasq** DHCP-Server
* **tio** Zugriff auf serielle Schnittstellen

**Wichtig:** Der Router darf keine Startup-Config besitzen (`Router# erase startup`). Weiterhin darf das Konfigurationsregister nicht auf `0x2142` (Startup-Config ignorieren) stehen.

**Status (3.5.26):** Auslieferung per Python Script funktioniert, der Router wird initial konfiguriert. Allerdings befindet er sich danach immer noch im Day0 Modus. Die Auslieferung per Config-Datei hat nicht funktioniert. Der Router fragt die Config-Datei nicht per HTTP ab, sondern versucht eine TFTP Verbindung aufzubauen.

## Flask

Es empfiehlt sich Flask in einem `venv` zu installieren:

* `python3 -m venv flask-venv`
* `source flask-venv/bin/activate`
* `pip install flask`


Der Python Flask server wird mit `python3 app.py` gestartet und wartet auf Port 80 auf eingehende Verbindungen.  
Es ist wichtig, dass die ausgelieferte URL mit der URL in der Konfiguration des DHCP-Servers übereinstimmt.


## dnsmasq

Der DHCP-Server kann mit `homebrew` auf MacOS installiert werden.
Im Verzeichnis `etc` befindet sich eine Beispielkonfiguration. Diese kann beim Aufruf von `dnsmasq` mit `-C` angegeben werden.

`sudo /opt/homebrew/opt/dnsmasq/sbin/dnsmasq --keep-in-foreground -C /opt/homebrew/etc/dnsmasq-ztp.conf`

## tio - Serial Terminal

Für den Zugriff auf die Cisco Console empfielt sich [tio](https://github.com/tio/tio):

* Anzeige der devices: `tio --list`  
* Verbinden: `tio --baudrate 9600 /dev/cu.usbserial-FTF8T2BZ`
* Verbindung trennen: `ctrl-t q`