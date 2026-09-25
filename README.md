# Network Diagnostic Toolkit

Diagnóstico puntual de red: hostname local, interfaces IPv4/IPv6, resolución de nombres, ping, conexión TCP y ruta hasta un destino. Implementado en Python 3.10+ con `socket`, `subprocess` y `psutil`. Compatible con Linux y Windows; no depende de un servidor externo para las consultas locales.

## Instalación y requisitos

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows: `py -m venv .venv` y `.venv\Scripts\Activate.ps1`. `ping` y `traceroute` deben estar en PATH en Linux (`iputils-ping` y `traceroute` en Debian/Ubuntu); Windows utiliza `ping` y `tracert`. Si falta una herramienta se informa y la consulta termina con salida 1.

## Uso y ejemplos

```bash
python network.py hostname
python network.py interfaces
python network.py dns localhost
python network.py ping 127.0.0.1
python network.py tcp localhost 8000
python network.py trace 127.0.0.1
```

Para probar TCP, abrir otra terminal y ejecutar `python -m http.server 8000 --bind 127.0.0.1` en una carpeta sin datos sensibles; cerrar con Ctrl+C. La herramienta sólo establece y cierra una conexión, no envía peticiones de aplicación.

El timeout TCP es de 3 segundos por intento de dirección. DNS usa el resolver del sistema y sus propios tiempos de espera. Ping envía cuatro paquetes y traceroute limita la ruta a 12 saltos; los procesos externos tienen un límite global de 45 segundos. ICMP bloqueado o saltos sin respuesta no implican que el servicio TCP esté caído.

Usar sólo destinos propios o autorizados. No hay barridos de rangos, descubrimiento automático de puertos ni funciones de explotación. Salida 0 indica consulta exitosa, 1 un error de consulta; los comandos externos conservan su código de salida y argumentos inválidos devuelven 2.

## Qué demuestra

DNS, IPv4/IPv6, diferencia entre ICMP y TCP, puertos, rutas, timeouts y ejecución de comandos sin shell. Las pruebas se pueden repetir localmente con los ejemplos de este README; el diagnóstico informa cuando una utilidad del sistema no está instalada.
