import time

# Assuming the Vcdj class is in the vcdj.py file within the prodj.core directory
from prodj.core.vcdj import Vcdj

def main():
    # Create a virtual CDJ instance
    virtual_cdj = Vcdj(None)  # Pass 'None' if the 'prodj' object is not used initially

    # Configure mock interface data
    virtual_cdj.set_interface_data("192.168.1.100", "255.255.255.0", "00:1A:79:AD:FE:ED")

    # Assuming the ports are set within the Vcdj or prodj object
    print("Starting all packet types send test loop...")

    try:
        while True:
            # Send every type of packet handled by Vcdj
            virtual_cdj.send_keepalive_packet()
            virtual_cdj.query_link_info(1, 'slot1')  # Modify as per actual slot values
            virtual_cdj.command_load_track(1, 'track1')  # Example values, adjust as needed
            virtual_cdj.command_fader_start_single(1, start=True)
            time.sleep(1)  # Wait a second before next loop iteration
    except KeyboardInterrupt:
        print("Test loop stopped by user.")

if __name__ == "__main__":
    main()