# Despliegue del Bot WOL

## Opción 1: Railway (recomendada, la más fácil)

1. Ve a https://railway.app y regístrate (con GitHub)
2. Crea un "New Project" → "Deploy from GitHub repo"
3. Selecciona el repo con estos archivos
4. Railway detecta el Dockerfile automáticamente
5. En el dashboard, ve a "Variables" y añade: `CLOUD_MODE=true`
6. La URL del servicio NO es necesaria, el bot se conecta solo

## Opción 2: Fly.io

```bash
flyctl launch --dockerfile Dockerfile
flyctl secrets set CLOUD_MODE=true
flyctl deploy
```

## Router Movistar - Puerto forwarding

1. Abre navegador y ve a http://192.168.1.1
2. Credenciales: admin / (la clave que viene en la pegatina del router)
3. Ve a: **Configuración avanzada → NAT → Mapeo de puertos**
4. Añade regla:
   - Nombre: `WOL`
   - Puerto externo: `9` (UDP)
   - Puerto interno: `9` (UDP)
   - IP destino: `192.168.1.37`
5. Guarda

## BIOS - Activar WOL

1. Reinicia el PC y pulsa `Supr` (Del) al arrancar para entrar en BIOS
2. Busca: **Power Management → Resume by PCI/PCI-E Device** → Enabled
3. **Power On By Onboard LAN** → Enabled  
4. **ERP** → Disabled (esto apaga el chip de red en S5)
5. F10 para guardar y salir

## Probar

Envía `/start` a @SigaroPoroBot en Telegram.

Cuando el PC esté apagado, envía `/wake` y debería encenderse.
