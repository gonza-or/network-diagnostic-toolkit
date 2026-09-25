#!/usr/bin/env python3
"""Diagnóstico de un destino de red indicado por el usuario."""

import argparse
import platform
import re
import shutil
import socket
import subprocess

import psutil


def host_value(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._:%-]*", value):
        raise argparse.ArgumentTypeError("Usar hostname o IP sin espacios, URL ni opciones")
    return value


def port_value(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("El puerto debe ser un entero") from None
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("Puerto fuera del rango 1–65535")
    return port


def run_command(command):
    if not shutil.which(command[0]):
        raise RuntimeError(f"No está disponible el comando {command[0]}")
    return subprocess.run(command, timeout=45, check=False).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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
                ips = [a.address for a in addresses if a.family in (socket.AF_INET, socket.AF_INET6)]
                print(f"{name}: {', '.join(ips) or 'Sin IP'}")
        elif args.action == "dns":
            addresses = socket.getaddrinfo(args.host, None, type=socket.SOCK_STREAM)
            for ip in sorted({address[4][0] for address in addresses}):
                print(ip)
        elif args.action == "tcp":
            with socket.create_connection((args.host, args.port), timeout=3) as connection:
                print(f"TCP conectado: {connection.getpeername()}")
        elif args.action == "ping":
            command = ["ping", "-n", "4", "-w", "2000"] if windows else ["ping", "-c", "4", "-W", "2"]
            return run_command(command + [args.host])
        elif args.action == "trace":
            command = ["tracert", "-d", "-h", "12", "-w", "1000"] if windows else ["traceroute", "-n", "-m", "12", "-w", "1", "-q", "1"]
            return run_command(command + [args.host])
    except (OSError, RuntimeError, psutil.Error, subprocess.TimeoutExpired) as error:
        print(f"No se pudo completar el diagnóstico: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
