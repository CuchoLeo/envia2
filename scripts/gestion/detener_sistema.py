#!/usr/bin/env python3
"""
Script para detener el sistema de seguimiento de OC
Detiene todos los procesos relacionados con la aplicación

Uso:
    python detener_sistema.py              # Modo interactivo (pide confirmación)
    python detener_sistema.py --force      # Modo forzado (sin confirmación)
    python detener_sistema.py -f           # Alias de --force
"""
import os
import sys
import signal
import subprocess
import time


def obtener_procesos_python():
    """Obtiene todos los procesos Python del sistema"""
    try:
        # Buscar procesos Python relacionados con el sistema
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )

        procesos_sistema = []
        lineas = result.stdout.split('\n')

        for linea in lineas:
            # Buscar procesos relacionados con nuestro sistema
            if 'python' in linea.lower() and any(archivo in linea for archivo in [
                'app.py',
                'email_monitor.py',
                'scheduler.py',
                'uvicorn'
            ]):
                partes = linea.split()
                if len(partes) >= 2:
                    try:
                        pid = int(partes[1])
                        comando = ' '.join(partes[10:])
                        procesos_sistema.append({
                            'pid': pid,
                            'comando': comando
                        })
                    except (ValueError, IndexError):
                        continue

        return procesos_sistema

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al obtener procesos: {e}")
        return []


def detener_proceso(pid, nombre="proceso"):
    """Detiene un proceso de forma ordenada"""
    try:
        print(f"   🛑 Deteniendo {nombre} (PID: {pid})...", end=' ')

        # Enviar SIGTERM para detención ordenada
        os.kill(pid, signal.SIGTERM)

        # Esperar hasta 5 segundos para que termine
        for _ in range(10):
            time.sleep(0.5)
            try:
                # Verificar si el proceso sigue vivo
                os.kill(pid, 0)
            except ProcessLookupError:
                print("✅ Detenido")
                return True

        # Si no terminó, forzar con SIGKILL
        print("⚠️  Forzando detención...", end=' ')
        os.kill(pid, signal.SIGKILL)
        time.sleep(0.5)
        print("✅ Terminado")
        return True

    except ProcessLookupError:
        print("✅ Ya estaba detenido")
        return True
    except PermissionError:
        print("❌ Sin permisos")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def detener_por_archivo_pid():
    """Intenta detener procesos usando archivos PID si existen"""
    archivos_pid = [
        'app.pid',
        'monitor.pid',
        'scheduler.pid'
    ]

    procesos_detenidos = []

    for archivo_pid in archivos_pid:
        if os.path.exists(archivo_pid):
            try:
                with open(archivo_pid, 'r') as f:
                    pid = int(f.read().strip())

                nombre = archivo_pid.replace('.pid', '')
                if detener_proceso(pid, nombre):
                    procesos_detenidos.append(pid)

                # Eliminar archivo PID
                os.remove(archivo_pid)

            except Exception as e:
                print(f"❌ Error al procesar {archivo_pid}: {e}")

    return procesos_detenidos


def main():
    """Función principal"""
    # Verificar si se pasa argumento --force
    force_mode = '--force' in sys.argv or '-f' in sys.argv

    print("\n" + "="*60)
    print("  🛑 DETENIENDO SISTEMA DE SEGUIMIENTO DE OC")
    if force_mode:
        print("  (Modo forzado - sin confirmación)")
    print("="*60 + "\n")

    # Paso 1: Intentar detener usando archivos PID
    print("📋 Paso 1: Buscando archivos PID...")
    pids_detenidos = detener_por_archivo_pid()

    if pids_detenidos:
        print(f"✅ Detenidos {len(pids_detenidos)} procesos usando archivos PID\n")
    else:
        print("ℹ️  No se encontraron archivos PID\n")

    # Paso 2: Buscar procesos activos
    print("📋 Paso 2: Buscando procesos activos del sistema...")
    procesos = obtener_procesos_python()

    # Filtrar procesos ya detenidos
    procesos_pendientes = [p for p in procesos if p['pid'] not in pids_detenidos]

    if not procesos_pendientes:
        print("✅ No se encontraron procesos activos del sistema\n")
    else:
        print(f"\n   Se encontraron {len(procesos_pendientes)} procesos activos:\n")

        for proceso in procesos_pendientes:
            print(f"   PID {proceso['pid']}: {proceso['comando'][:70]}...")

        print()

        # Confirmar detención (a menos que esté en modo forzado)
        if not force_mode:
            respuesta = input("   ¿Detener estos procesos? (S/n): ").strip().lower()
        else:
            respuesta = 's'
            print("   Deteniendo procesos automáticamente (modo forzado)...\n")

        if respuesta in ['s', 'si', 'y', 'yes', '']:
            print()
            detenidos = 0
            for proceso in procesos_pendientes:
                nombre = f"Proceso {proceso['pid']}"
                if detener_proceso(proceso['pid'], nombre):
                    detenidos += 1
                    time.sleep(0.5)  # Pequeña pausa entre procesos

            print(f"\n✅ {detenidos} de {len(procesos_pendientes)} procesos detenidos exitosamente")
        else:
            print("\n❌ Operación cancelada por el usuario")

    # Paso 3: Verificación final
    print("\n📋 Paso 3: Verificación final...")
    time.sleep(1)

    procesos_restantes = obtener_procesos_python()

    if not procesos_restantes:
        print("✅ Sistema detenido completamente")
    else:
        print(f"⚠️  Aún hay {len(procesos_restantes)} procesos activos:")
        for proceso in procesos_restantes:
            print(f"   • PID {proceso['pid']}: {proceso['comando'][:60]}...")

    print("\n" + "="*60)
    print("  ✅ PROCESO DE DETENCIÓN COMPLETADO")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operación interrumpida por el usuario\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}\n")
        sys.exit(1)
