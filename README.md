Autonomo

Autonomo es un orquestador de ejecuciones escrito en Python.

Su objetivo es proporcionar un nucleo simple, modular y extensible para ejecutar tareas, coordinar procesos y mantener un estado persistente del sistema.

Objetivos

- Orquestar tareas de forma secuencial o automatica.
- Mantener un ciclo continuo de ejecucion.
- Registrar el estado del sistema.
- Facilitar la incorporacion de nuevos modulos.
- Servir como base para agentes autonomos.

Estructura

autonomo/
|
+-- main.py
+-- runner.py
+-- core.py
+-- config.py
+-- tasks/
|   +-- __init__.py
|
+-- state/
|
+-- logs/
|
+-- README.md

Componentes

core.py

Contiene el estado global y los servicios comunes utilizados por el sistema.

runner.py

Coordina la ejecucion de las tareas registradas.

tasks/

Conjunto de modulos independientes. Cada tarea implementa un metodo:

def run():
    ...

Filosofia

Cada componente tiene una unica responsabilidad.

- El Core mantiene el estado.
- El Runner ejecuta.
- Las tareas realizan trabajo.
- Los modulos permanecen desacoplados.

Esta separacion permite extender el sistema sin modificar el nucleo.

Requisitos

- Python 3.10 o superior.
- Sin dependencias externas.

Licencia

MIT License.
