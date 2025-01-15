import subprocess

def list_networks():
    result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], stdout=subprocess.PIPE)
    print(result.stdout.decode())

def connect_to_network(ssid, password):
    try:
        subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password], check=True)
        print(f"Connected to {ssid} successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to connect to {ssid}.")

def main():
    while True:
        print("Available networks:")
        list_networks()
        ssid = input("Enter the SSID of the network you want to connect to (or 'q' to quit): ")
        if ssid.lower() == 'q':
            break
        password = input(f"Enter the password for {ssid}: ")
        connect_to_network(ssid, password)

if __name__ == "__main__":
    main()
