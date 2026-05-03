from flask import Flask, render_template, request

app = Flask(__name__)

# Einfache Router-Datenbank
DEVICES = {
    "FCZ2944R08Q": {"hostname": "Berlin-Edge-01", "mgmt_ip": "192.168.1.10"},
    "SN67890DEF": {"hostname": "Hamburg-Branch-02", "mgmt_ip": "192.168.1.11"}
}

# 1. Klassische Config ausliefern
# hat bisher nicht funktioniert, Router versucht Config per TFTP zu laden
@app.route('/configs/router_config.conf')
def serve_config():
    # Hier liest du einfach eine normale .txt oder .cfg Datei ein
    with open("my_router_config.txt", "r") as f:
        config_content = f.read()
    
    # WICHTIG: Der Content-Type muss text/plain sein
    return config_content, 200, {'Content-Type': 'text/plain'}

# 2. Python Bootstrap-Skript ausliefern(Guestshell)
# Startup-Config muss leer sein (erase startup) und Config-Register darf
# nicht auf 0x2142 (skip Startup) eingestellt sein
@app.route('/provision/bootstrap.py')
def bootstrap():
    with open('bootstrap_client.py', 'r') as f:
        # WICHTIG: Content-Type muss text/x-python sein
        return f.read(), 200, {'Content-Type': 'text/x-python'}

# 3. Die finale Config ausliefern (wird vom Bootstrap-Skript aufgerufen)
# abhängig von der Seriennummer des Routers unterschiedliche Einstellungen
@app.route('/get_final_config/<sn>')
def get_config(sn):
    device = DEVICES.get(sn)
    if device:
        print(f"Konfiguration für {sn} wird generiert...")
        # Template mit Daten füllen und als HTTP-Response zurückgeben
        # Jinja Template wird im Verzeichnis './templates' gesucht
        with app.app_context():
            return render_template('cisco_config.j2', **device), 200, {'Content-Type': 'text/plain'}
    else:
        return "Device unknown", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
