# Network Diagnostic Toolkit

Script de Python para revisar una conexión de red.

Permite consultar hostname e interfaces, resolver DNS, hacer ping, probar un puerto TCP y ejecutar traceroute/tracert.

## Requisitos

- Python 3.10 o superior
- `psutil`
- En Linux: `ping` y `traceroute`
- En Windows: `ping` y `tracert`

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Uso

```bash
python network.py hostname
python network.py interfaces
python network.py dns localhost
python network.py ping 127.0.0.1
python network.py tcp localhost 8000
python network.py trace 127.0.0.1
```

Para probar TCP, abrir un servidor local en otra terminal:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

El script no hace barridos ni envía datos de aplicación. Usá equipos propios o autorizados. Si falta un comando, muestra el error y termina con código 1.
