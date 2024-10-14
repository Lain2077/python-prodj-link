
import socket
import time
from prodj.network.packets import KeepAlivePacket, BeatPacket

# Server details
SERVER_IP = '169.254.1.105'  # Change to your server IP
SERVER_PORT = 50001          # Change to your server port
INTERVAL = 5                 # Time between packets in seconds

def send_packet(sock, packet_data, server_address):
    try:
        sock.sendto(packet_data, server_address)
        print("Packet sent to {0}:{1}".format(server_address[0], server_address[1]))
    except Exception as e:
        print("Failed to send packet: {0}".format(e))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_address = (SERVER_IP, SERVER_PORT)
        
        while True:
            # Prepare a KeepAlive packet
            keep_alive_packet = KeepAlivePacket().prepare()
            send_packet(sock, keep_alive_packet, server_address)
            
            # Prepare a Beat packet
            beat_packet = BeatPacket().prepare()
            send_packet(sock, beat_packet, server_address)
            
            time.sleep(INTERVAL)

if __name__ == '__main__':
    main()