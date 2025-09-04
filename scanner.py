import socket
import threading
import argparse

# Common ports dictionary for service detection
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

open_ports = []

def grab_banner(sock, ip, port):
    try:
        sock.send(b"Hello\r\n")
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = common_ports.get(port, "Unknown")
            banner = grab_banner(sock, ip, port)
            if banner:
                output = f"[+] Port {port} OPEN ({service}) | Banner: {banner}"
            else:
                output = f"[+] Port {port} OPEN ({service})"
            print(output)
            open_ports.append(output)
        sock.close()
    except:
        pass

def run_scanner(target, start_port, end_port, threads=100):
    print(f"\n[INFO] Scanning {target} from {start_port} to {end_port}...\n")

    thread_list = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        thread_list.append(t)
        t.start()

        # Control number of active threads
        if len(thread_list) >= threads:
            for t in thread_list:
                t.join()
            thread_list = []

    for t in thread_list:
        t.join()

    # Save results
    with open("scan_results.txt", "w") as f:
        for line in open_ports:
            f.write(line + "\n")
    print(f"\n[INFO] Scan complete. Results saved to scan_results.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("-t", "--target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Port range, e.g. 1-1000")
    args = parser.parse_args()

    if args.target and args.ports:
        target = args.target
        start_port, end_port = map(int, args.ports.split("-"))
    else:
        # Replit-friendly interactive input
        print("Welcome to the Python Network Scanner!")
        target = input("Enter target host (default: scanme.nmap.org): ") or "scanme.nmap.org"
        port_range = input("Enter port range (e.g. 1-100): ") or "1-100"
        start_port, end_port = map(int, port_range.split("-"))

    run_scanner(target, start_port, end_port)


