#!/usr/bin/env python3
import os
import sys
import asyncio
import subprocess
from pathlib import Path

def setup_redbot():
    """Configurar Red-DiscordBot con las variables de entorno"""
    
    # Variables requeridas
    token = os.getenv('DISCORD_TOKEN')
    owner_id = os.getenv('OWNER_ID') 
    prefix = os.getenv('BOT_PREFIX', '!')
    instance_name = os.getenv('INSTANCE_NAME', 'renderbot')
    
    if not token:
        print("❌ ERROR: DISCORD_TOKEN no encontrado")
        sys.exit(1)
    
    if not owner_id:
        print("❌ ERROR: OWNER_ID no encontrado")
        sys.exit(1)
    
    print(f"🤖 Configurando bot: {instance_name}")
    print(f"📝 Prefijo: {prefix}")
    
    # Crear directorio de datos
    data_path = Path("./data")
    data_path.mkdir(exist_ok=True)
    
    return token, owner_id, prefix, instance_name

async def main():
    token, owner_id, prefix, instance_name = setup_redbot()
    
    # Ejecutar redbot directamente
    cmd = [
        "python", "-m", "redbot",
        instance_name,
        "--token", token,
        "--prefix", prefix,
        "--owner", owner_id,
        "--no-prompt",
        "--no-cogs-install"
    ]
    
    print(f"🚀 Ejecutando: {' '.join(cmd[:3])} {instance_name} [ARGS OCULTOS]")
    
    try:
        # Ejecutar el comando
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Mostrar output en tiempo real
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
        
        process.wait()
        
    except KeyboardInterrupt:
        print("🛑 Bot detenido por el usuario")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
