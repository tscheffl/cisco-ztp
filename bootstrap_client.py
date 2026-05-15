import cli
import urllib.request
import re

def get_serial():
    # Cisco-Befehl ausfuehren
    inventory = cli.execute("show inventory")
    # Nach der Seriennummer (RegEx) suchen
    match = re.search(r'SN:\s+(\w+)', inventory)
    return match.group(1) if match else None

def main():
    sn = get_serial()
    if not sn:
        print("Konnte Seriennummer nicht finden!")
        return

    print(f"Geraet erkannt: {sn}. Fordere Config an...")
    
    # URL zum Flask-Server (IP deines Macs anpassen!)
    url = f"http://192.168.1.100:5000/get_final_config/{sn}"
    
    try:
        response = urllib.request.urlopen(url)
        config = response.read().decode('utf-8')
        
        # Die Konfiguration auf dem Router anwenden
        print("Wende Konfiguration an...")
        cli.configure(config)
        print("ZTP abgeschlossen!")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
