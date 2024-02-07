//blackbox.ai generated

import socket

def log_nmap_scan(source_ip):
    with open("nmap_scans.log", "a") as log_file:
        log_file.write(f"Nmap scan detected from {source_ip} at {datetime.now()}\n")

def monitor_network():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind(("", 0))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            packet = sock.recvfrom(65565)[0]
            ip_header = packet[0:20]
            iph = struct.unpack("!BBHHHBBH4s4s", ip_header)

            version_ihl = iph[0]
            version = version_ihl >> 4
            ihl = version_ihl & 0xF

            iph_length = ihl * 4
            total_length = iph[2]
            identification = iph[3]
            flags_fo = iph[4]
            fragment_offset = flags_fo & 0x1FFF
            ttl = iph[5]
            protocol = iph[6]
            checksum = iph[7]
            source_ip = socket.inet_ntoa(iph[8])
            destination_ip = socket.inet_ntoa(iph[9])

            if protocol == 17: # Protocol 17 is UDP, which Nmap often uses
                udp_header = packet[iph_length:iph_length+8]
                udph = struct.unpack("!HHHH", udp_header)

                source_port = udph[0]
                destination_port = udph[1]

                if destination_port == 11211: # Nmap often scans for port 11211 (Memcached)
                    log_nmap_scan(source_ip)

    finally:
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == "__main__":
    monitor_network()
