#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Verificar variables de entorno requeridas
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERROR: DISCORD_TOKEN no encontrado en variables de entorno")
        sys.exit(1)
    
    owner_id = os.getenv('OWNER_ID')
    if not owner_id:
        print("❌ ERROR: OWNER_ID no encontrado en variables de entorno")  
        sys.exit(1)
    
    prefix = os.getenv('BOT_PREFIX', '!')
    instance_name = os.getenv('INSTANCE_NAME', 'renderbot')
    
    print(f"🤖 Iniciando bot con prefijo: {prefix}")
    print(f"📁 Instancia: {instance_name}")
    
    # Importar después de verificar variables
    try:
        from redbot.__main__ import main as red_main
        
        # Configurar argumentos para redbot
        sys.argv = [
            'redbot',
            instance_name,
            '--token', token,
            '--prefix', prefix, 
            '--owner', owner_id,
            '--no-prompt'
        ]
        
        # Ejecutar redbot
        await red_main()
        
    except ImportError as e:
        print(f"❌ Error al importar Red-DiscordBot: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al iniciar el bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)
