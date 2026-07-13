# WOL Telegram Bot

Enciende este PC remotamente via Telegram.

## Requisitos

1. **Router**: Reenviar puerto UDP 9 a `192.168.1.37`
2. **BIOS**: Activar "Power On By PCIe/Resume by PCI"
3. **Cloud**: Cuenta gratuita en [Railway](https://railway.app) o [Fly.io](https://fly.io)

## Puerto forwarding en el router

Abre el puerto UDP 9 entrante y reenvíalo a `192.168.1.37` puerto 9.

Si el router no lo permite, alternativas:
- Usar UPnP (ya activo en este PC)
- Configurar el router como DMZ para este PC (no recomendado)

## Comandos del bot

- `/wake` - Envía magic packet WOL para encender el PC
- `/status` - Ping al PC para ver si está encendido

## Despliegue

### Railway (más fácil)

```bash
# 1. Sube esta carpeta a un repo de GitHub
# 2. Ve a https://railway.app -> New Project -> Deploy from GitHub repo
# 3. Railway detecta el Dockerfile automáticamente y lo despliega
```

### Fly.io

```bash
flyctl launch --dockerfile Dockerfile
flyctl deploy
```
