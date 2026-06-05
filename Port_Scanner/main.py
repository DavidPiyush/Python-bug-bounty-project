#!/usr/bin/env python3
# port_scanner.py — Build Nmap from scratch

import socket
import concurrent.futures
import argparse
import time
from datetime import datetime

# Common port → service mapping
SERVICES = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
    53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
    135: 'DCE/RPC Mapper',139:'NetBIOS',
    443: 'HTTPS', 445: 'SMB',903:'VMRC',913:"APEX-Edge", 3306: 'MySQL',
    3389: 'RDP', 5432: 'PostgreSQL',5040:'CDPSvc', 6379: 'Redis',
    8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
}

def grab_banner(ip, port, timeout=2):
    """Grab service banner if available"""
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))

        # HTTP banner
        if port in [80, 8080, 8443]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner[:80] if banner else None
    except:
        return None

def scan_port(ip, port, timeout=1):
    """Check if port is open"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0    # 0 = open
    except:
        return False

def scan_target(ip, ports, threads=100, grab_banners=False):
    """Scan multiple ports concurrently"""
    open_ports = []

    print(f"\n{'='*55}")
    print(f"  Target: {ip}")
    print(f"  Ports:  {len(ports)}")
    print(f"  Start:  {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*55}")

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(scan_port, ip, p): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            if future.result():
                service = SERVICES.get(port, 'Unknown')
                banner = grab_banner(ip, port) if grab_banners else None

                open_ports.append(port)
                print(f"  ✅ {port:5d}/tcp  OPEN  {service}")
                if banner:
                    print(f"          Banner: {banner[:60]}")

    elapsed = time.time() - start
    print(f"\n  Found {len(open_ports)} open ports in {elapsed:.2f}s")
    return sorted(open_ports)

def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("target", help="Target IP")
    parser.add_argument("-p", "--ports",
                        default="1-1024",
                        help="Port range (default: 1-1024)")
    parser.add_argument("-t", "--threads",
                        type=int, default=100)
    parser.add_argument("-b", "--banners",
                        action="store_true",
                        help="Grab service banners")
    args = parser.parse_args()

    # Parse port range
    if '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
        ports = range(start, end + 1)
    elif ',' in args.ports:
        ports = [int(p) for p in args.ports.split(',')]
    else:
        ports = [int(args.ports)]

    scan_target(args.target, ports,
                args.threads, args.banners)

if __name__ == "__main__":
    main()