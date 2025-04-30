#!/bin/python

import argparse
from scapy.all import *

def send_dns_query_packet(query_name, dns_server, port, txid, ipaddr, ns):
    # Make DNS packet
    txid = txid if txid else RandShort()
    dns_query = DNS(id=txid, qr=0, qd=DNSQR(qname=query_name, qtype="A"))
    
    ip = IP(dst=dns_server)
    udp = UDP(sport=RandShort(), dport=port)
    
    packet = ip/udp/dns_query
    print("ACTUAL PACKET BEING SENT:")
    packet.show()  # This will display the full packet structure
    send(packet, verbose=0)
    print(f"Sent DNS packet to {dns_server}:{port} with query name {query_name}")
    
def send_dns_response_packet(query_name, dns_server, port, rcode, txid, ipaddr, ns):
    txid = txid if txid else RandShort()
    
    # Build DNS response components
    qd = DNSQR(qname=query_name, qtype="A")  # Question section
    
    # Answer section (from -i)
    an = DNSRR(
        rrname=query_name,
        type="A",
        rclass="IN",
        ttl=3600,
        rdata=ipaddr
    ) if ipaddr else None
    
    # Authority section (from -n)
    ns_rr = DNSRR(
        rrname=query_name,
        type="NS",
        rclass="IN",
        ttl=3600,
        rdata=ns
    ) if ns else None
    
    # Construct complete DNS packet
    dns_response = DNS(
        id=txid,
        qr=1,  # Response flag
        aa=1,  # Authoritative answer
        rcode=rcode,
        qd=qd,  # Question
        an=an,  # Answer (from -i)
        ns=ns_rr,  # Authority (from -n)
        ancount=1 if ipaddr else 0,
        nscount=1 if ns else 0
    )
    
    ip = IP(dst=dns_server)
    udp = UDP(sport=RandShort(), dport=port)
    packet = ip/udp/dns_response
    print("ACTUAL PACKET BEING SENT:")
    packet.show()  # This will display the full packet structure
    send(packet, verbose=0)
    print(f"Sent DNS response packet to {dns_server}:{port} with query name {query_name}")
    



def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="DNS Query/Response Tool")
    
    # Define expected arguments
    parser.add_argument("query_name", help="The DNS query name (e.g., example.com)")
    parser.add_argument("dns_server", help="The DNS server to query (e.g., localhost)")

    # Define options with flags
    parser.add_argument("-p", "--port", type=int, default=53, help="Specify destination port (default: 53)")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--query", action="store_true", help="Send as query packet")
    group.add_argument("-r", "--response", action="store_true", help="Send as response packet")
    
    parser.add_argument("-c", "--rcode", type=int, default=0, help="Set response code (0-15, default: 0)")
    parser.add_argument("-t", "--txid", type=int, help="Set transaction ID (0-65535, default: any)")
    parser.add_argument("-i", "--ipaddr", help="IP address to include in response")
    parser.add_argument("-n", "--ns", help="Nameserver to include in response")

    # Parse the arguments
    args = parser.parse_args()
    
    # Default to query mode if neither -q nor -r is specified
    if not args.query and not args.response:
        args.query = True  # Default behavior
    
    if args.response:
        args.response = True
    elif args.query:
        args.query = True

    # Print out the parsed arguments (you can replace this with actual functionality)
    print(f"Query Name: {args.query_name}")
    print(f"DNS Server: {args.dns_server}")
    print(f"Port: {args.port}")
    print(f"Query Mode: {args.query}")
    print(f"Response Mode: {args.response}")
    print(f"Response Code (rcode): {args.rcode}")
    print(f"Transaction ID (txid): {args.txid}")
    print(f"IP Address: {args.ipaddr}")
    print(f"Nameserver: {args.ns}")
    
    if args.query:
        send_dns_query_packet(
            query_name=args.query_name,
            dns_server=args.dns_server,
            port=args.port,
            txid=args.txid,
            ipaddr=args.ipaddr,
            ns=args.ns
        )
    else:
        send_dns_response_packet(
            query_name=args.query_name,
            dns_server=args.dns_server,
            port=args.port,
            rcode=args.rcode,
            txid=args.txid,
            ipaddr=args.ipaddr,
            ns=args.ns
        )

if __name__ == "__main__":
    main()
