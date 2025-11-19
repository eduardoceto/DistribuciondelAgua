'''
1. Instancias

Tipos de Nodo :
FuentesNodos no-fuente

Tuberias (aristas):
Peso asociados, simbolizado la capacidad de la tuberia.

-Numero de nodos y aristas
-[NODES]: Listado de nodos. Cada uno contiene un id de nodo, sus coordenadas en x,
y y un numero booleano que indica si el nodo es una fuente o no.
-[EDGES]: Listado de aristas. Cada una esta formada por los ids de dos nodos 
y un tercer numero que representa su capacidad (diámetro).
-[OFFICE]: El id de un nodo donde se encuentra la oficina base. 
-[NEW]:  Una lista de nuevos nodos para ser agregados a la red. 
Por cada uno se indican sus coordenadas x,y, y el diámetro de la tubería que se usaría para conectarlo. Ninguno de los nodos nuevos es una fuente. 
'''

import os
from typing import List, Dict


class Nodo:
    def __init__(self, id_nodo: int, x: float, y: float, es_fuente: bool):
        self.id = id_nodo
        self.x = x
        self.y = y
        self.es_fuente = es_fuente


class Arista:
    def __init__(self, nodo1: int, nodo2: int, capacidad: float):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.capacidad = capacidad
        self.longitud = None


class NuevoNodo:
    def __init__(self, x: float, y: float, diametro: float):
        self.x = x
        self.y = y
        self.diametro = diametro


class Instancia:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.num_nodos = 0
        self.num_aristas = 0
        self.nodos: Dict[int, Nodo] = {}
        self.aristas: List[Arista] = []
        self.office_id = None
        self.nuevos_nodos: List[NuevoNodo] = []
    
    def agregar_nodo(self, id_nodo: int, x: float, y: float, es_fuente: bool):
        self.nodos[id_nodo] = Nodo(id_nodo, x, y, es_fuente)
    
    def agregar_arista(self, nodo1: int, nodo2: int, capacidad: float):
        self.aristas.append(Arista(nodo1, nodo2, capacidad))
    
    def agregar_nuevo_nodo(self, x: float, y: float, diametro: float):
        self.nuevos_nodos.append(NuevoNodo(x, y, diametro))
    
    def obtener_fuentes(self) -> List[Nodo]:
        return [nodo for nodo in self.nodos.values() if nodo.es_fuente]


def leer_instancia(ruta_archivo: str) -> Instancia:
    """
    Lee y parsea un archivo de instancia.
    
    Args:
        ruta_archivo: Ruta al archivo .txt de la instancia
        
    Returns:
        Instancia: Objeto Instancia con todos los datos parseados
    """
    # Obtener el nombre de la instancia desde el nombre del archivo
    nombre = os.path.splitext(os.path.basename(ruta_archivo))[0]
    instancia = Instancia(nombre)
    
    with open(ruta_archivo, 'r') as f:
        lineas = f.readlines()
    
    seccion_actual = None
    i = 0
    
    primera_linea = lineas[i].strip().split()
    instancia.num_nodos = int(primera_linea[0])
    instancia.num_aristas = int(primera_linea[1])
    i += 1
    
    while i < len(lineas):
        linea = lineas[i].strip()
        
        if not linea:
            i += 1
            continue
        
        if linea == "[NODES]":
            seccion_actual = "NODES"
            i += 1
            continue
        elif linea == "[EDGES]":
            seccion_actual = "EDGES"
            i += 1
            continue
        elif linea == "[OFFICE]":
            seccion_actual = "OFFICE"
            i += 1
            continue
        elif linea == "[NEW]":
            seccion_actual = "NEW"
            i += 1
            continue
        
        if seccion_actual == "NODES":
            partes = linea.split()
            id_nodo = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            es_fuente = int(partes[3]) == 1
            instancia.agregar_nodo(id_nodo, x, y, es_fuente)
        
        elif seccion_actual == "EDGES":
            partes = linea.split()
            nodo1 = int(partes[0])
            nodo2 = int(partes[1])
            capacidad = float(partes[2])
            instancia.agregar_arista(nodo1, nodo2, capacidad)
        
        elif seccion_actual == "OFFICE":
            instancia.office_id = int(linea)
        
        elif seccion_actual == "NEW":
            partes = linea.split()
            x = float(partes[0])
            y = float(partes[1])
            diametro = float(partes[2])
            instancia.agregar_nuevo_nodo(x, y, diametro)
        
        i += 1
    
    return instancia


def cargar_todas_las_instancias(directorio: str = "instancias") -> Dict[str, Instancia]:
    """
    Carga todas las instancias desde un directorio.
    
    Args:
        directorio: Directorio que contiene los archivos .txt de instancias
        
    Returns:
        Dict[str, Instancia]: Diccionario con nombre de instancia como clave
    """
    instancias = {}
    archivos = [f for f in os.listdir(directorio) if f.endswith('.txt')]
    
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        instancia = leer_instancia(ruta_completa)
        instancias[instancia.nombre] = instancia
    
    return instancias




'''
2. Longitud de las tuberias

Utiliza las coordenadas x,y de cada nodo para calcular la distancia entre ellos.

Salidas: un listado de aristas, agregando la longitud a sus atributos preexistentes. 


'''



'''
3. Sectorizacion

En la division de la red en sectores asociados a cada fuente.

Los nodos deben ser suministrados por la fuente mas cercana, con respecto a la red. 
La separación entre sectores se consigue cerrando algunas tuberías. Determina cuales.
Debes reportar cuales nodos pertenecen al mismo sector, 
cuales tuberías quedan cerradas, y mostrarlo visualmente (grafico de colores, marcando las 
tuberías cerradas, estilo libre)

Salidas: lista cuales nodos pertenecen al mismo sector y cuales tuberías quedan cerradas. 
'''



'''
4. Frescura de agua

Una métrica de la calidad del agua es el tiempo que tarda en llegar de la fuente a un nodo. 
Esto es proporcional a la distancia de la fuente al nodo.

Salidas: Por cada sector, su fuente, nodo mas lejano y la longitud de esa distancia. 
'''


'''
5. Flujo maximo de cada sector
Utiliza la capacidad de las diferentes tuberías para determinar el flujo máximo de cada sector
Considera como
Origen: la fuente
Destino: el nodo mas alejado de la fuente

Salidas:  Por cada sector, sus nodos origen, destino, y flujo máximo. 
Además, por cada tubería (arista) del sector, cuanta de su capacidad se utiliza. Ej. 50 de 200.
'''


'''
6. Mustra de calidad de agua

Para analizar la calidad del agua, se deben tomar muestras de cada nodo.
Determina una ruta de distancia mínima para que una persona, ubicada 
en el nodo marcado como "office" visite toda la red tomando muestras y regrese.
Supón que puede hacerlo en un solo día, y que los patrones de las calles coinciden con las tuberías

Salidas: La secuencia de visita de los nodos, con la distancia de cada arista en el recorrido y el total de su suma. 
'''


'''
7. Expansion de la red
Suponiendo que se crea un nuevo nodo en
coordenadas especificas
¿Cómo se conectaría a la red? Enlaza el nuevo nodo al nodo mas cercano que no sea una fuente.
Después, actualiza la red apropiadamente

Se repiten los pasos 2, 3, 4, 5 y 6 para la nueva red.

Salidas: Las aristas nuevas del nodo, y su longitud. Para mostrar la actualización, crea dos archivos con el antes y el después. 
'''



'''
Coloca las salidas en dos archivos de texto (antes y después de agregar los nodos nuevos). Dale a estos archivos nombres que coincidan con el nombre las instancias de prueba.
Guarda las salidas de los puntos anteriores en un formato legible y ordenado, especificando a que punto corresponden y que datos se están mostrando.

Genera graficas donde se aprecien visualmente las salidas:

a) Los nodos, sus conexiones, longitudes, capacidades.
b) Cuales nodos son fuentes, nodos mas lejanos, cuales pertenecen al mismo sector. 
c) Cual es el recorrido del punto 6, la longitud de las aristas involucradas, y longitud total. 
e) La red actualizada con los nodos nuevos. 

Guarda las imágenes en archivos jpg o png. 


'''