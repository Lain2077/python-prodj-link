import socket
import time
from prodj.network.packets import KeepAlivePacket, BeatPacket, StatusPacket

def send_packet(sock, packet_data, ip, port):
    try:
        print(f"Sending packet to {ip}:{port}")
        sock.sendto(packet_data, (ip, port))
        print("Packet sent successfully!")
    except Exception as e:
        print(f"Failed to send packet: {e}")

def send_keepalive(sock, ip, port, player_number, model="CDJ-2000"):
    data = {
        "type": "type_status",
        "subtype": "stype_status",
        "model": model,
        "content": {
            "player_number": player_number,
            "ip_addr": ip,
            "mac_addr": "00:11:22:33:44:55",  # Example MAC address
        }
    }
    packet = KeepAlivePacket.build(data)
    send_packet(sock, packet, ip, port)

def send_beat(sock, ip, port, player_number, model="CDJ-2000"):
    data = {
        "type": "type_beat",
        "subtype": "stype_beat",
        "model": model,
        "player_number": player_number,
        "content": {
            "next_beat": 1000,
            "bpm": 128,
            "beat": 1,
            "pitch": 1.0,
            "distances": [0, 0, 0, 0]  # Add 'distances' as required
        }
    }
    packet = BeatPacket.build(data)
    send_packet(sock, packet, ip, port)



def send_status(sock, ip, port, player_number, model="CDJ-2000"):
    data = {
        "type": "cdj",
        "subtype": "stype_status",
        "model": model,
        "player_number": player_number,
        "extra": {   # Added based on the necessity of the structure.
            "u3": 0,
            "player_number2": player_number  # Example dummy data
        },
        "content": {
            "track_id": 12345,
            "track_number": 1,
            "bpm": 128,
            "physical_pitch": 1.02,
            "beat": 4,
        }
    }
    packet = StatusPacket.build(data)
    send_packet(sock, packet, ip, port)

if __name__ == "__main__":
    # Define the target IPs and ports based on the logs
    local_ip = "192.168.1.101"  # Your current IP
    cdj_ip1 = "192.168.1.230"  # XDJ1
    cdj_ip2 = "192.168.1.232"  # XDJ2
    target_port_beat = 50001
    target_port_status = 50002
    player_number_xdj1 = 1  # You can set the player number manually
    player_number_xdj2 = 2

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Simulate sending packets to both XDJs
    # For XDJ1 (169.254.16.26)
    print("Sending packets to XDJ1")
    #send_keepalive(sock, cdj_ip1, target_port_status, player_number_xdj1)
    #time.sleep(1)
    #send_beat(sock, cdj_ip1, target_port_beat, player_number_xdj1)
    #time.sleep(1)
    send_status(sock, cdj_ip1, target_port_status, player_number_xdj1)

    # For XDJ2 (169.254.15.253)
    print("Sending packets to XDJ2")
    #send_keepalive(sock, cdj_ip2, target_port_status, player_number_xdj2)
    #time.sleep(1)
    #send_beat(sock, cdj_ip2, target_port_beat, player_number_xdj2)
    time.sleep(1)
    send_status(sock, cdj_ip2, target_port_status, player_number_xdj2)

    sock.close()
