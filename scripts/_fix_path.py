"""
Módulo auxiliar para agregar la raíz del proyecto al path de Python
Importa este módulo al inicio de cualquier script en scripts/

Uso:
    import sys
    import os

    # Agregar raíz del proyecto al path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # Cambiar directorio de trabajo a la raíz del proyecto
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
"""

def fix_path():
    """
    Agrega la raíz del proyecto al sys.path y cambia el CWD a la raíz

    Esto permite que los scripts se ejecuten desde cualquier directorio
    sin problemas de imports o rutas relativas.
    """
    import sys
    import os

    # Calcular ruta de la raíz del proyecto (3 niveles arriba de este archivo)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Agregar al path si no está ya
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Cambiar directorio de trabajo
    os.chdir(project_root)

    return project_root
