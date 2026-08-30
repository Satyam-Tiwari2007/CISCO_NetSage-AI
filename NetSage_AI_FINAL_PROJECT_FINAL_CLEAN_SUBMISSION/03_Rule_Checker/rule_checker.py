"""
NetSage AI — Deterministic Network Rule Checker
Cisco VIP Internship Project

Purpose:
    Perform deterministic checks for common configuration mistakes
    before/alongside AI diagnosis.

Supported checks:
    - duplicate IP addresses
    - subnet mask mismatch
    - default gateway mismatch
    - interface down
    - missing VLAN
    - missing route

This script is intentionally rule-based and does not use an AI/LLM.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class CheckResult:
    check: str
    status: str       # PASS / WARNING / ERROR
    message: str


def parse_ipv4(value: str) -> Optional[ipaddress.IPv4Address]:
    try:
        return ipaddress.ip_address(value.strip())
    except ValueError:
        return None


def check_duplicate_ips(ip_addresses: List[str]) -> CheckResult:
    cleaned = [x.strip() for x in ip_addresses if parse_ipv4(x)]
    duplicates = sorted({ip for ip in cleaned if cleaned.count(ip) > 1})

    if duplicates:
        return CheckResult(
            "duplicate_ip",
            "ERROR",
            f"Duplicate IP address(es) detected: {', '.join(duplicates)}"
        )

    return CheckResult(
        "duplicate_ip",
        "PASS",
        "No duplicate IPv4 addresses detected."
    )


def check_subnet_mask(
    host_ip: str,
    subnet_mask: str,
    expected_network: str
) -> CheckResult:
    try:
        interface = ipaddress.ip_interface(f"{host_ip}/{subnet_mask}")
        expected = ipaddress.ip_network(expected_network, strict=False)
    except ValueError:
        return CheckResult(
            "subnet_mask",
            "ERROR",
            "Invalid IP address, subnet mask, or expected network."
        )

    if interface.network != expected:
        return CheckResult(
            "subnet_mask",
            "WARNING",
            f"Host resolves to {interface.network}, expected {expected}."
        )

    return CheckResult(
        "subnet_mask",
        "PASS",
        f"Host belongs to expected network {expected}."
    )


def check_default_gateway(
    host_ip: str,
    subnet_mask: str,
    gateway: str
) -> CheckResult:
    try:
        network = ipaddress.ip_network(
            f"{host_ip}/{subnet_mask}", strict=False
        )
        gw = parse_ipv4(gateway)
        if gw is None:
            raise ValueError
    except ValueError:
        return CheckResult(
            "gateway_mismatch",
            "ERROR",
            "Invalid host IP, subnet mask, or gateway."
        )

    if gw not in network:
        return CheckResult(
            "gateway_mismatch",
            "WARNING",
            f"Gateway {gateway} is outside host network {network}."
        )

    return CheckResult(
        "gateway_mismatch",
        "PASS",
        f"Gateway {gateway} belongs to host network {network}."
    )


def check_interface_status(interface_name: str, status_text: str) -> CheckResult:
    text = status_text.lower()

    if "administratively down" in text:
        return CheckResult(
            "interface_status",
            "ERROR",
            f"{interface_name} is administratively down."
        )

    if re.search(r"\bdown\b", text) and "up, line protocol is up" not in text:
        return CheckResult(
            "interface_status",
            "WARNING",
            f"{interface_name} appears to be down."
        )

    if "up, line protocol is up" in text:
        return CheckResult(
            "interface_status",
            "PASS",
            f"{interface_name} is operationally up."
        )

    return CheckResult(
        "interface_status",
        "WARNING",
        f"Unable to conclusively determine {interface_name} status."
    )


def check_vlan_exists(
    vlan_id: int,
    show_vlan_output: str
) -> CheckResult:
    pattern = rf"(?m)^\s*{re.escape(str(vlan_id))}\s+\S+"

    if re.search(pattern, show_vlan_output):
        return CheckResult(
            "vlan_exists",
            "PASS",
            f"VLAN {vlan_id} is present in the supplied VLAN table."
        )

    return CheckResult(
        "vlan_exists",
        "WARNING",
        f"VLAN {vlan_id} was not found in the supplied VLAN table."
    )


def check_route_exists(
    destination: str,
    show_ip_route_output: str
) -> CheckResult:
    try:
        network = ipaddress.ip_network(destination, strict=False)
    except ValueError:
        return CheckResult(
            "route_exists",
            "ERROR",
            f"Invalid destination network: {destination}"
        )

    # Deliberately simple parser for Cisco-style route evidence.
    network_text = str(network)
    compact = show_ip_route_output.replace(" ", "")

    if network_text in show_ip_route_output or network_text.replace("/", "/") in compact:
        return CheckResult(
            "route_exists",
            "PASS",
            f"Evidence contains a route for {network_text}."
        )

    # Also check common Cisco route notation such as 192.168.2.0/24.
    if re.search(
        rf"{re.escape(str(network.network_address))}\s*/\s*{network.prefixlen}",
        show_ip_route_output
    ):
        return CheckResult(
            "route_exists",
            "PASS",
            f"Evidence contains a route for {network_text}."
        )

    return CheckResult(
        "route_exists",
        "WARNING",
        f"No route for {network_text} was found in the supplied output."
    )


def run_case(
    *,
    ip_addresses: Optional[List[str]] = None,
    host_ip: Optional[str] = None,
    subnet_mask: Optional[str] = None,
    expected_network: Optional[str] = None,
    gateway: Optional[str] = None,
    interface_name: Optional[str] = None,
    interface_status: Optional[str] = None,
    vlan_id: Optional[int] = None,
    show_vlan_output: Optional[str] = None,
    destination: Optional[str] = None,
    show_ip_route_output: Optional[str] = None,
) -> List[CheckResult]:

    results = []

    if ip_addresses is not None:
        results.append(check_duplicate_ips(ip_addresses))

    if host_ip and subnet_mask and expected_network:
        results.append(
            check_subnet_mask(host_ip, subnet_mask, expected_network)
        )

    if host_ip and subnet_mask and gateway:
        results.append(
            check_default_gateway(host_ip, subnet_mask, gateway)
        )

    if interface_name and interface_status:
        results.append(
            check_interface_status(interface_name, interface_status)
        )

    if vlan_id is not None and show_vlan_output is not None:
        results.append(
            check_vlan_exists(vlan_id, show_vlan_output)
        )

    if destination and show_ip_route_output is not None:
        results.append(
            check_route_exists(destination, show_ip_route_output)
        )

    return results


def print_report(results: List[CheckResult]) -> None:
    print("=" * 72)
    print("NetSage AI — Deterministic Rule Checker")
    print("=" * 72)

    for result in results:
        print(f"[{result.status:<7}] {result.check:<20} {result.message}")

    errors = sum(r.status == "ERROR" for r in results)
    warnings = sum(r.status == "WARNING" for r in results)
    passed = sum(r.status == "PASS" for r in results)

    print("-" * 72)
    print(f"PASS: {passed} | WARNING: {warnings} | ERROR: {errors}")
    print("=" * 72)


def demo() -> None:
    """Run a reproducible demonstration of all six checks."""

    results = run_case(
        ip_addresses=[
            "192.168.10.20",
            "192.168.10.21",
            "192.168.10.20",  # duplicate
        ],
        host_ip="192.168.20.25",
        subnet_mask="255.255.255.0",  # correct /24 for this check
        expected_network="192.168.30.0/24",
        gateway="192.168.10.1",     # outside host network
        interface_name="GigabitEthernet0/1",
        interface_status="GigabitEthernet0/1 is administratively down",
        vlan_id=20,
        show_vlan_output="""
10 SALES active
30 USERS active
""",                              # VLAN 20 missing
        destination="192.168.30.0/24",
        show_ip_route_output="""
C 192.168.10.0/24 is directly connected
C 192.168.20.0/24 is directly connected
""",                              # route missing
    )

    print_report(results)


if __name__ == "__main__":
    demo()
