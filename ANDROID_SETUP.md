# Relay Android para WOL

## Requisitos
- Android con conexión WiFi (misma red que el PC)
- Termux (F-Droid, NO Play Store)
- Cuenta de Telegram con número de teléfono

## 1. Instalar Termux
Desde F-Droid: https://f-droid.org/packages/com.termux/

## 2. Obtener API_ID y API_HASH
1. Ir a https://my.telegram.org/apps
2. Iniciar sesión con tu número de teléfono
3. Crear una aplicación si no tienes una
4. Copiar **api_id** y **api_hash**

## 3. Configurar Termux
Abrir Termux y pegar:

```bash
pkg update && pkg upgrade -y
pkg install python python-pip git -y
pip install telethon
```

## 4. Descargar el script

```bash
cd ~
curl -o android_relay.py https://raw.githubusercontent.com/SigaroPoro/wol-bot/main/android_relay.py
```

## 5. Editar API_ID y API_HASH

```bash
nano android_relay.py
```

Cambiar las líneas:
```python
API_ID = 12345  # <- Tu api_id
API_HASH = "tu_api_hash_aqui"  # <- Tu api_hash
```

Guardar: Ctrl+X, Y, Enter

## 6. Ejecutar

```bash
python android_relay.py
```

La primera vez pedirá:
1. Número de teléfono (con código de país, ej: +34612345678)
2. Código de verificación de Telegram

Después de eso, se queda corriendo escuchando mensajes.

## 7. Mantenerlo corriendo en segundo plano

Para que no se cierre al cerrar Termux:

```bash
nohup python android_relay.py > relay.log 2>&1 &
```

O instalar Termux:Boot para que arranque automáticamente.

## Cómo funciona
1. Tú envías `/wake` al bot
2. El bot (Railway) envía "🚀 WAKE" al chat
3. El Android ve el mensaje y envía WOL como **broadcast local**
4. El PC se enciende (aunque está apagado y el router no tenga ARP)
