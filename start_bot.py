#!/usr/bin/env python3
import os
import sys
import asyncio
import subprocess
from pathlib import Path

# Configuración del bot
BOT_NAME = "achopapi"
DEFAULT_PREFIX = "/"

def setup_environment():
    """Configura el entorno para Red-DiscordBot"""
    # Variables de entorno necesarias
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: Variable de entorno DISCORD_TOKEN no encontrada")
        print("   Configúrala en Render.com Dashboard > Environment")
        sys.exit(1)
    
    # Configurar directorio de datos persistente
    data_dir = Path("/opt/render/project/src/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar variables de entorno para Red
    os.environ['RED_DATA_PATH'] = str(data_dir)
    
    print(f"🤖 Bot: {BOT_NAME}")
    print(f"📝 Prefijo: {DEFAULT_PREFIX}")
    print(f"💾 Datos: {data_dir}")
    
    return token

def setup_bot_instance():
    """Configura la instancia del bot si no existe"""
    try:
        # Verificar si la instancia ya existe
        from redbot.core import data_manager
        data_manager.load_basic_configuration(BOT_NAME)
        print("✅ Instancia del bot ya configurada")
        return True
    except:
        print("🔧 Configurando nueva instancia del bot...")
        
        # Crear instancia con configuración mínima
        setup_cmd = [
            sys.executable, "-m", "redbot", "setup",
            "--no-prompt",
            "--instance-name", BOT_NAME,
            "--data-dir", os.environ['RED_DATA_PATH']
        ]
        
        try:
            result = subprocess.run(setup_cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)
            
            if result.returncode == 0:
                print("✅ Instancia configurada correctamente")
                return True
            else:
                print(f"❌ Error configurando instancia: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout configurando instancia")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def run_bot():
    """Ejecuta el bot"""
    token = setup_environment()
    
    # Configurar instancia si es necesaria
    if not setup_bot_instance():
        print("❌ No se pudo configurar la instancia del bot")
        sys.exit(1)
    
    print("🚀 Iniciando Red-DiscordBot...")
    
    # Ejecutar el bot
    cmd = [
        sys.executable, "-m", "redbot", BOT_NAME,
        "--token", token,
        "--prefix", DEFAULT_PREFIX
    ]
    
    try:
        # Ejecutar en modo no-daemon para Render
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el bot: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("🛑 Bot detenido")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("🔴 RED DISCORD BOT - RENDER.COM")
    print("=" * 50)
    run_bot()
