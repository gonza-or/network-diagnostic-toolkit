#!/usr/bin/env python3
import argparse
import platform
import re
import shutil
import socket
import subprocess

import psutil


def host_value(value):
    if not re.fullmatch(r"[a-zA-Z0-9:][a-zA-Z0-9._:%-]*", value):
        raise argparse.ArgumentTypeError("Usar hostname o IP sin espacios, URL ni opciones")
    return value


def port_value(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("El puerto debe ser un entero")
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Puerto fuera del rango 1-65535")
    return port


def run_command(command):
    if not shutil.which(command[0]):
        raise RuntimeError("No está disponible el comando {}".format(command[0]))
    return subprocess.run(command, timeout=45, check=False).returncode


def main():
    parser = argparse.ArgumentParser(description="Consulta una conexión de red")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("hostname", help="Hostname del equipo local")
    commands.add_parser("interfaces", help="IP de las interfaces locales")
    for name in ("dns", "ping", "trace", "tcp"):
        command = commands.add_parser(name)
        command.add_argument("host", type=host_value)
        if name == "tcp":
            command.add_argument("port", type=port_value)
    args = parser.parse_args()
    windows = platform.system() == "Windows"
    try:
        if args.action == "hostname":
            print(socket.gethostname())
        elif args.action == "interfaces":
            for name, addresses in psutil.net_if_addrs().items():
                ips = []
                for address in addresses:
                    if address.family in (socket.AF_INET, socket.AF_INET6):
                        ips.append(address.address)
                if ips:
                    value = ", ".join(ips)
                else:
                    value = "Sin IP"
                print("{}: {}".format(name, value))
        elif args.action == "dns":
            addresses = socket.getaddrinfo(args.host, None, type=socket.SOCK_STREAM)
            ips = []
            for address in addresses:
                ip = address[4][0]
                if ip not in ips:
                    ips.append(ip)
            for ip in sorted(ips):
                print(ip)
        elif args.action == "tcp":
            with socket.create_connection((args.host, args.port), timeout=3) as connection:
                print("TCP conectado: {}".format(connection.getpeername()))
        elif args.action == "ping":
            if windows:
                command = ["ping", "-n", "4", "-w", "2000"]
            else:
                command = ["ping", "-c", "4", "-W", "2"]
            return run_command(command + [args.host])
        elif args.action == "trace":
            if windows:
                command = ["tracert", "-d", "-h", "12", "-w", "1000"]
            else:
                command = ["traceroute", "-n", "-m", "12", "-w", "1", "-q", "1"]
            return run_command(command + [args.host])
    except (OSError, RuntimeError, psutil.Error, subprocess.TimeoutExpired) as error:
        print("Error: {}".format(error))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
