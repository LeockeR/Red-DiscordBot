#!/usr/bin/env python3
import os
import asyncio
import sys
from pathlib import Path

# Agregar el directorio redbot al path
sys.path.insert(0, str(Path(__file__).parent / "redbot"))

async def main():
    from redbot.core.bot import Red
    from redbot.core.global_checks import init_global_checks
    from redbot.core.config import Config
    from redbot.core.data_manager import appdir
    
    # Configuración desde variables de entorno
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("ERROR: DISCORD_TOKEN no encontrado en variables de entorno")
        sys.exit(1)
    
    prefix = os.getenv('BOT_PREFIX', '!')
    owner_id = os.getenv('OWNER_ID')
    
    if not owner_id:
        print("ERROR: OWNER_ID no encontrado en variables de entorno")
        sys.exit(1)
    
    # Crear directorio de datos si no existe
    data_path = Path(os.getenv('REDBOT_DATA_PATH', './data'))
    data_path.mkdir(exist_ok=True)
    
    # Configurar Red
    bot = Red(
        cli_flags=type('', (), {
            'token': token,
            'prefix': [prefix],
            'owner': [int(owner_id)],
            'no_prompt': True,
            'instance_name': os.getenv('INSTANCE_NAME', 'renderbot'),
            'data_path': str(data_path)
        })()
    )
    
    init_global_checks(bot)
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()

if __name__ == "__main__":
    asyncio.run(main())
