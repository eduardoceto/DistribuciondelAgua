from cProfile import label
import os
import math
from typing import List, Dict, Set, Tuple
import matplotlib.pyplot as plt
from collections import defaultdict, deque
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
        self.num_aristas += 1
    
    def agregar_nuevo_nodo(self, x: float, y: float, diametro: float):
        self.nuevos_nodos.append(NuevoNodo(x, y, diametro))
    
    def agregar_nodo_expansion(self, x: float, y: float, 
                               es_fuente: bool = False) -> int:
        nuevo_id = max(self.nodos.keys(), default=0) + 1
        self.agregar_nodo(nuevo_id, x, y, es_fuente)
        self.num_nodos += 1
        return nuevo_id
    
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
    
    instancia.num_aristas = len(instancia.aristas)
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


def copiar_instancia(instancia: Instancia) -> Instancia:
    copia = Instancia(instancia.nombre)
    copia.num_nodos = instancia.num_nodos
    copia.num_aristas = instancia.num_aristas
    copia.office_id = instancia.office_id
    
    for nodo_id, nodo in instancia.nodos.items():
        copia.nodos[nodo_id] = Nodo(nodo.id, nodo.x, nodo.y, nodo.es_fuente)
    
    for arista in instancia.aristas:
        copia.aristas.append(Arista(arista.nodo1, arista.nodo2, 
                                   arista.capacidad))
        copia.aristas[-1].longitud = arista.longitud
    
    for nuevo in instancia.nuevos_nodos:
        copia.nuevos_nodos.append(NuevoNodo(nuevo.x, nuevo.y, nuevo.diametro))
    
    return copia


'''
2. Longitud de las tuberias

Utiliza las coordenadas x,y de cada nodo para calcular la distancia entre ellos.

Salidas: un listado de aristas, agregando la longitud a sus atributos preexistentes. 


'''

def distancia_euclidiana(x1: float, y1: float, x2: float, y2: float) -> float:
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def calcular_longitud_arista(instancia: Instancia, 
                             arista: Arista) -> float:
    nodo1 = instancia.nodos[arista.nodo1]
    nodo2 = instancia.nodos[arista.nodo2]
    return distancia_euclidiana(nodo1.x, nodo1.y, nodo2.x, nodo2.y)


def calcular_longitudes_tuberias(instancia: Instancia) -> None:
    for arista in instancia.aristas:
        if arista.longitud is None:
            arista.longitud = calcular_longitud_arista(instancia, arista)


def encontrar_nodo_cercano(instancia: Instancia, x: float, 
                           y: float) -> Tuple[int, float]:
    nodo_cercano_id = None
    distancia_min = float('inf')
    
    for nodo_id, nodo in instancia.nodos.items():
        if not nodo.es_fuente:
            dist = distancia_euclidiana(x, y, nodo.x, nodo.y)
            if dist < distancia_min:
                distancia_min = dist
                nodo_cercano_id = nodo_id
    
    return nodo_cercano_id, distancia_min


def obtener_ruta_resultados(instancia: Instancia, etapa: str = "antes",
                            directorio_base: str = "resultados") -> str:
    directorio = os.path.join(directorio_base, instancia.nombre, etapa)
    os.makedirs(directorio, exist_ok=True)
    return directorio


def obtener_ruta_grafica(instancia: Instancia, tipo: str, 
                        etapa: str = "antes",
                        directorio_base: str = "resultados") -> str:
    directorio = obtener_ruta_resultados(instancia, etapa, directorio_base)
    return os.path.join(directorio, f"{tipo}.png")


def graficar_red(instancia: Instancia, ruta_salida: str = None,
                 mostrar_etiquetas: bool = True, etapa: str = "antes") -> None:
    fig, ax = plt.subplots(figsize=(14, 12))
    
    calcular_longitudes_tuberias(instancia)
    
    max_capacidad = max(a.capacidad for a in instancia.aristas)
    min_capacidad = min(a.capacidad for a in instancia.aristas)
    
    for arista in instancia.aristas:
        nodo1 = instancia.nodos[arista.nodo1]
        nodo2 = instancia.nodos[arista.nodo2]
        
        capacidad_norm = arista.capacidad / max_capacidad
        color = plt.cm.viridis(capacidad_norm)
        grosor = 1 + capacidad_norm * 3
        
        ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y], 
                color=color, linewidth=grosor, alpha=0.7, zorder=1)
        
        if mostrar_etiquetas:
            mid_x = (nodo1.x + nodo2.x) / 2
            mid_y = (nodo1.y + nodo2.y) / 2
            etiqueta = f"L:{arista.longitud:.1f}\nC:{arista.capacidad:.1f}"
            ax.text(mid_x, mid_y, etiqueta, fontsize=6, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8),
                    zorder=3)
    
    fuentes_dibujadas = False
    for id_nodo, nodo in instancia.nodos.items():
        if nodo.es_fuente:
            label = 'Fuente' if not fuentes_dibujadas else ''
            ax.scatter(nodo.x, nodo.y, c='red', s=250, marker='s',
                      edgecolors='black', linewidths=2, zorder=4,
                      label=label)
            fuentes_dibujadas = True
        else:
            ax.scatter(nodo.x, nodo.y, c='blue', s=120, marker='o',
                      edgecolors='black', linewidths=1.5, zorder=4)
        
        ax.text(nodo.x, nodo.y, str(id_nodo), fontsize=9,
                ha='center', va='center', color='white',
                weight='bold', zorder=5)
    
    if instancia.office_id in instancia.nodos:
        office = instancia.nodos[instancia.office_id]
        ax.scatter(office.x, office.y, c='green', s=300, marker='*',
                  edgecolors='black', linewidths=2, zorder=6, label='Oficina')
    
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, 
                               norm=plt.Normalize(vmin=min_capacidad, 
                                                 vmax=max_capacidad))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.02, shrink=0.6)
    cbar.set_label('Capacidad', fontsize=9, weight='bold')
    cbar.ax.tick_params(labelsize=8)
    
    ax.set_xlabel('Coordenada X', fontsize=12)
    ax.set_ylabel('Coordenada Y', fontsize=12)
    titulo = (f'Red de Distribución de Agua - {instancia.nombre}\n'
              f'Nodos: {len(instancia.nodos)}, '
              f'Aristas: {len(instancia.aristas)} | '
              f'Longitudes calculadas')
    ax.set_title(titulo, fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if ruta_salida is None:
        ruta_salida = obtener_ruta_grafica(instancia, "red", etapa)
    
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', format='png')
    print(f"Gráfica guardada en: {ruta_salida}")
    plt.close()



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

def construir_grafo(instancia: Instancia) -> Dict[int, List[int]]:
    grafo = defaultdict(list)
    for arista in instancia.aristas:
        grafo[arista.nodo1].append(arista.nodo2)
        grafo[arista.nodo2].append(arista.nodo1)
    return grafo


def distancia_en_red(instancia: Instancia, grafo: Dict[int, List[int]],
                    nodo_inicio: int, nodo_fin: int) -> float:
    if nodo_inicio == nodo_fin:
        return 0.0
    
    calcular_longitudes_tuberias(instancia)
    
    distancias = {nodo_inicio: 0.0}
    cola = deque([nodo_inicio])
    
    while cola:
        actual = cola.popleft()
        
        for vecino in grafo.get(actual, []):
            if vecino not in distancias:
                arista = next((a for a in instancia.aristas 
                              if (a.nodo1 == actual and a.nodo2 == vecino) or
                                 (a.nodo1 == vecino and a.nodo2 == actual)), None)
                if arista and arista.longitud:
                    nueva_dist = distancias[actual] + arista.longitud
                    distancias[vecino] = nueva_dist
                    if vecino == nodo_fin:
                        return nueva_dist
                    cola.append(vecino)
    
    return float('inf')


def camino_en_red(instancia: Instancia, grafo: Dict[int, List[int]],
                 nodo_inicio: int, nodo_fin: int) -> Tuple[List[int], float]:
    if nodo_inicio == nodo_fin:
        return [nodo_inicio], 0.0
    
    calcular_longitudes_tuberias(instancia)
    
    distancias = {nodo_inicio: 0.0}
    predecesores = {nodo_inicio: None}
    cola = deque([nodo_inicio])
    
    while cola:
        actual = cola.popleft()
        
        for vecino in grafo.get(actual, []):
            if vecino not in distancias:
                arista = next((a for a in instancia.aristas 
                              if (a.nodo1 == actual and a.nodo2 == vecino) or
                                 (a.nodo1 == vecino and a.nodo2 == actual)), None)
                if arista and arista.longitud:
                    nueva_dist = distancias[actual] + arista.longitud
                    distancias[vecino] = nueva_dist
                    predecesores[vecino] = actual
                    if vecino == nodo_fin:
                        camino = []
                        nodo = nodo_fin
                        while nodo is not None:
                            camino.append(nodo)
                            nodo = predecesores[nodo]
                        return list(reversed(camino)), nueva_dist
                    cola.append(vecino)
    
    return [], float('inf')


def sectorizar_red(instancia: Instancia) -> Tuple[Dict[int, int], Set[Tuple[int, int]]]:
    calcular_longitudes_tuberias(instancia)
    fuentes = instancia.obtener_fuentes()
    grafo = construir_grafo(instancia)
    
    if not fuentes:
        return {}, set()
    
    distancias = {}
    cola = deque()
    
    for fuente in fuentes:
        distancias[fuente.id] = (0.0, fuente.id)
        cola.append((fuente.id, fuente.id))
    
    while cola:
        nodo_actual, fuente_origen = cola.popleft()
        dist_actual, _ = distancias[nodo_actual]
        
        for vecino in grafo.get(nodo_actual, []):
            arista = next((a for a in instancia.aristas 
                          if (a.nodo1 == nodo_actual and a.nodo2 == vecino) or
                             (a.nodo1 == vecino and a.nodo2 == nodo_actual)), None)
            
            if arista and arista.longitud:
                nueva_dist = dist_actual + arista.longitud
                
                if vecino not in distancias or nueva_dist < distancias[vecino][0]:
                    distancias[vecino] = (nueva_dist, fuente_origen)
                    cola.append((vecino, fuente_origen))
    
    asignacion_sector = {}
    for nodo_id, (_, fuente_id) in distancias.items():
        asignacion_sector[nodo_id] = fuente_id
    
    for fuente in fuentes:
        asignacion_sector[fuente.id] = fuente.id
    
    aristas_cerradas = set()
    for arista in instancia.aristas:
        sector1 = asignacion_sector.get(arista.nodo1)
        sector2 = asignacion_sector.get(arista.nodo2)
        if sector1 and sector2 and sector1 != sector2:
            aristas_cerradas.add((min(arista.nodo1, arista.nodo2),
                                 max(arista.nodo1, arista.nodo2)))
    
    return asignacion_sector, aristas_cerradas


def graficar_sectorizacion(instancia: Instancia, ruta_salida: str = None, 
                          etapa: str = "antes") -> None:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    fuentes = instancia.obtener_fuentes()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    calcular_longitudes_tuberias(instancia)
    
    colores_sectores = ['#1f77b4', '#d62728', '#ff7f0e', '#2ca02c', 
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    fuente_a_color = {}
    for i, fuente in enumerate(fuentes):
        fuente_a_color[fuente.id] = colores_sectores[i % len(colores_sectores)]
    
    for arista in instancia.aristas:
        par = (min(arista.nodo1, arista.nodo2),
               max(arista.nodo1, arista.nodo2))
        if par not in aristas_cerradas:
            nodo1 = instancia.nodos[arista.nodo1]
            nodo2 = instancia.nodos[arista.nodo2]
            sector = asignacion_sector[arista.nodo1]
            color = fuente_a_color.get(sector, 'gray')
            ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
                   color=color, linewidth=2, alpha=0.6, zorder=1)
    
    for nodo1_id, nodo2_id in aristas_cerradas:
        nodo1 = instancia.nodos[nodo1_id]
        nodo2 = instancia.nodos[nodo2_id]
        ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
               color='black', linewidth=2, linestyle='--',
               alpha=0.4, zorder=1)
    
    for id_nodo, nodo in instancia.nodos.items():
        sector = asignacion_sector.get(id_nodo)
        color = fuente_a_color.get(sector, 'gray')
        
        if nodo.es_fuente:
            ax.scatter(nodo.x, nodo.y, c=color, s=400, marker='o',
                      edgecolors='black', linewidths=3, zorder=5)
        else:
            ax.scatter(nodo.x, nodo.y, c=color, s=150, marker='o',
                      edgecolors='black', linewidths=1.5, zorder=4)
        
        ax.text(nodo.x, nodo.y, str(id_nodo), fontsize=8,
                ha='center', va='center', color='white',
                weight='bold', zorder=6)
    
    if instancia.office_id in instancia.nodos:
        office = instancia.nodos[instancia.office_id]
        ax.scatter(office.x, office.y, c='yellow', s=350, marker='*',
                  edgecolors='black', linewidths=2, zorder=7, label='Oficina')
    
    ax.set_xlabel('Coordenada X', fontsize=12)
    ax.set_ylabel('Coordenada Y', fontsize=12)
    titulo = (f'Sectorización de la Red - {instancia.nombre}\n'
              f'Sectores: {len(fuentes)}, '
              f'Tuberías cerradas: {len(aristas_cerradas)}')
    ax.set_title(titulo, fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if ruta_salida is None:
        ruta_salida = obtener_ruta_grafica(instancia, "sectorizacion", etapa)
    
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', format='png')
    print(f"Gráfica de sectorización guardada en: {ruta_salida}")
    plt.close()


def reportar_sectorizacion(instancia: Instancia) -> Dict:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    fuentes = instancia.obtener_fuentes()
    
    sectores = defaultdict(list)
    for id_nodo, fuente_id in asignacion_sector.items():
        sectores[fuente_id].append(id_nodo)
    
    tuberias_cerradas = []
    for nodo1_id, nodo2_id in aristas_cerradas:
        tuberias_cerradas.append((nodo1_id, nodo2_id))
    
    return {
        'sectores': dict(sectores),
        'tuberias_cerradas': tuberias_cerradas,
        'num_sectores': len(fuentes),
        'num_tuberias_cerradas': len(aristas_cerradas)
    }



'''
4. Frescura de agua

Una métrica de la calidad del agua es el tiempo que tarda en llegar de la fuente a un nodo. 
Esto es proporcional a la distancia de la fuente al nodo.

Salidas: Por cada sector, su fuente, nodo mas lejano y la longitud de esa distancia. 
'''

def construir_grafo_sector(instancia: Instancia, 
                          aristas_cerradas: Set[Tuple[int, int]]) -> Dict[int, List[int]]:
    grafo = defaultdict(list)
    for arista in instancia.aristas:
        par = (min(arista.nodo1, arista.nodo2),
               max(arista.nodo1, arista.nodo2))
        if par not in aristas_cerradas:
            grafo[arista.nodo1].append(arista.nodo2)
            grafo[arista.nodo2].append(arista.nodo1)
    return grafo


def calcular_frescura_agua(instancia: Instancia) -> Dict:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    grafo = construir_grafo_sector(instancia, aristas_cerradas)
    fuentes = instancia.obtener_fuentes()
    calcular_longitudes_tuberias(instancia)
    
    resultados = {}
    
    for fuente in fuentes:
        distancias = {fuente.id: 0.0}
        predecesores = {fuente.id: None}
        cola = deque([fuente.id])
        
        while cola:
            actual = cola.popleft()
            for vecino in grafo.get(actual, []):
                if vecino not in distancias:
                    arista = next(
                        (a for a in instancia.aristas
                         if (a.nodo1 == actual and a.nodo2 == vecino) or
                            (a.nodo1 == vecino and a.nodo2 == actual)), None)
                    if arista and arista.longitud:
                        distancias[vecino] = distancias[actual] + arista.longitud
                        predecesores[vecino] = actual
                        cola.append(vecino)
        
        sector_nodos = [nid for nid, fid in asignacion_sector.items()
                        if fid == fuente.id and nid != fuente.id]
        
        max_dist = 0.0
        nodo_mas_lejano = None
        for nodo_id in sector_nodos:
            if nodo_id in distancias and distancias[nodo_id] > max_dist:
                max_dist = distancias[nodo_id]
                nodo_mas_lejano = nodo_id
        
        if nodo_mas_lejano:
            camino = []
            nodo = nodo_mas_lejano
            while nodo is not None:
                camino.append(nodo)
                nodo = predecesores.get(nodo)
            camino.reverse()
            
            resultados[fuente.id] = {
                'fuente': fuente.id,
                'nodo_mas_lejano': nodo_mas_lejano,
                'distancia': max_dist,
                'camino': camino
            }
    
    return resultados




def graficar_frescura_agua(instancia: Instancia, ruta_salida: str = None,
                          etapa: str = "antes") -> None:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    frescura = calcular_frescura_agua(instancia)
    fuentes = instancia.obtener_fuentes()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    calcular_longitudes_tuberias(instancia)
    
    colores_sectores = ['#1f77b4', '#d62728', '#ff7f0e', '#2ca02c', 
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    fuente_a_color = {}
    for i, fuente in enumerate(fuentes):
        fuente_a_color[fuente.id] = colores_sectores[i % len(colores_sectores)]
    
    for arista in instancia.aristas:
        par = (min(arista.nodo1, arista.nodo2),
               max(arista.nodo1, arista.nodo2))
        if par not in aristas_cerradas:
            nodo1 = instancia.nodos[arista.nodo1]
            nodo2 = instancia.nodos[arista.nodo2]
            sector = asignacion_sector[arista.nodo1]
            color = fuente_a_color.get(sector, 'gray')
            ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
                   color=color, linewidth=1.5, alpha=0.4, zorder=1)
    
    for nodo1_id, nodo2_id in aristas_cerradas:
        nodo1 = instancia.nodos[nodo1_id]
        nodo2 = instancia.nodos[nodo2_id]
        ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
               color='black', linewidth=1, linestyle='--',
               alpha=0.2, zorder=1)
    
    for fuente_id, info in frescura.items():
        camino = info['camino']
        color = fuente_a_color.get(fuente_id, 'gray')
        distancia_total = info['distancia']
        
        for i in range(len(camino) - 1):
            nodo1 = instancia.nodos[camino[i]]
            nodo2 = instancia.nodos[camino[i + 1]]
            ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
                   color=color, linewidth=4, alpha=0.8, zorder=2)
        
        if camino:
            nodo_fin = instancia.nodos[camino[-1]]
            ax.text(nodo_fin.x, nodo_fin.y + 100, 
                   f"Dist: {distancia_total:.1f}",
                   fontsize=10, ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.5', 
                            facecolor=color, alpha=0.8,
                            edgecolor='black', linewidth=2),
                   weight='bold', zorder=8)
    
    for id_nodo, nodo in instancia.nodos.items():
        sector = asignacion_sector.get(id_nodo)
        color = fuente_a_color.get(sector, 'gray')
        
        es_fuente = nodo.es_fuente
        es_mas_lejano = any(info['nodo_mas_lejano'] == id_nodo 
                           for info in frescura.values())
        
        if es_fuente:
            ax.scatter(nodo.x, nodo.y, c=color, s=500, marker='o',
                      edgecolors='black', linewidths=3, zorder=5)
        elif es_mas_lejano:
            ax.scatter(nodo.x, nodo.y, c=color, s=400, marker='s',
                      edgecolors='black', linewidths=3, zorder=5)
        else:
            ax.scatter(nodo.x, nodo.y, c=color, s=120, marker='o',
                      edgecolors='black', linewidths=1.5, zorder=4)
        
        ax.text(nodo.x, nodo.y, str(id_nodo), fontsize=8,
                ha='center', va='center', color='white',
                weight='bold', zorder=6)
    
    if instancia.office_id in instancia.nodos:
        office = instancia.nodos[instancia.office_id]
        ax.scatter(office.x, office.y, c='yellow', s=350, marker='*',
                  edgecolors='black', linewidths=2, zorder=7, label='Oficina')
    
    ax.set_xlabel('Coordenada X', fontsize=12)
    ax.set_ylabel('Coordenada Y', fontsize=12)
    
    info_frescura = '\n'.join([f"Fuente {info['fuente']} -> Nodo {info['nodo_mas_lejano']}: "
                              f"{info['distancia']:.1f} (distancia total)" 
                              for info in frescura.values()])
    
    titulo = (f'Frescura de Agua - {instancia.nombre}\n'
              f'{info_frescura}')
    ax.set_title(titulo, fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if ruta_salida is None:
        ruta_salida = obtener_ruta_grafica(instancia, "frescura", etapa)
    
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', format='png')
    print(f"Gráfica de frescura guardada en: {ruta_salida}")
    plt.close()


'''
5. Flujo maximo de cada sector
Utiliza la capacidad de las diferentes tuberías para determinar el flujo máximo de cada sector
Considera como
Origen: la fuente
Destino: el nodo mas alejado de la fuente

Salidas:  Por cada sector, sus nodos origen, destino, y flujo máximo. 
Además, por cada tubería (arista) del sector, cuanta de su capacidad se utiliza. Ej. 50 de 200.
'''

def calcular_flujo_maximo(instancia: Instancia) -> Dict:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    grafo_sector = construir_grafo_sector(instancia, aristas_cerradas)
    fuentes = instancia.obtener_fuentes()
    calcular_longitudes_tuberias(instancia)

    # Encontrar el nodo más lejano de la fuente en cada sector y su camino
    caminos_a_explorar = {}
    for fuente in fuentes:
        distancias = {fuente.id: 0.0}
        predecesores = {fuente.id: None}
        cola = deque([fuente.id])

        while cola:
            actual = cola.popleft()
            for vecino in grafo_sector.get(actual, []):
                if vecino not in distancias:
                    arista = next(
                        (a for a in instancia.aristas
                         if (a.nodo1 == actual and a.nodo2 == vecino) or
                            (a.nodo1 == vecino and a.nodo2 == actual)), None)
                    if arista and arista.longitud is not None:
                        distancias[vecino] = distancias[actual] + arista.longitud
                        predecesores[vecino] = actual
                        cola.append(vecino)

        sector_nodos = [nid for nid, fid in asignacion_sector.items() if fid == fuente.id and nid != fuente.id]

        max_dist = 0.0
        nodo_mas_lejano = None
        for nodo_id in sector_nodos:
            if nodo_id in distancias and distancias[nodo_id] > max_dist:
                max_dist = distancias[nodo_id]
                nodo_mas_lejano = nodo_id

        if nodo_mas_lejano:
            caminos_a_explorar[fuente.id] = {
                'nodo_mas_lejano': nodo_mas_lejano
            }

    # Helper: construir capacidades dirigidas para el sector (ambas direcciones igual a capacidad original)
    def construir_capacidades_para_sector(fuente_id: int):
        capacity = {}
        nodes_in_sector = {nid for nid, fid in asignacion_sector.items() if fid == fuente_id}
        adj = defaultdict(set)
        for ar in instancia.aristas:
            par = (min(ar.nodo1, ar.nodo2), max(ar.nodo1, ar.nodo2))
            if par in aristas_cerradas:
                continue
            if ar.nodo1 in nodes_in_sector and ar.nodo2 in nodes_in_sector:
                # crea aristas dirigidas en ambas direcciones con capacidad = ar.capacidad
                capacity[(ar.nodo1, ar.nodo2)] = ar.capacidad
                capacity[(ar.nodo2, ar.nodo1)] = ar.capacidad
                adj[ar.nodo1].add(ar.nodo2)
                adj[ar.nodo2].add(ar.nodo1)
        return capacity, adj

    # Implementación de Edmonds-Karp 
    def edmonds_karp(capacity: Dict[Tuple[int,int], float], adj: Dict[int, Set[int]], s: int, t: int):
        flow = defaultdict(float)  # flujo actual por arista (u,v)
        max_flow = 0.0

        while True:
            parent = {}
            q = deque([s])
            parent[s] = None
            # BFS para encontrar camino aumentante en la red
            while q and t not in parent:
                u = q.popleft()
                for v in adj.get(u, []):
                    cap = capacity.get((u, v), 0.0)
                    used = flow.get((u, v), 0.0)
                    residual = cap - used
                    if residual > 1e-9 and v not in parent:
                        parent[v] = u
                        q.append(v)
            if t not in parent:
                break  # no hay más caminos

            # encuentra bottleneck
            v = t
            bottleneck = float('inf')
            while parent[v] is not None:
                u = parent[v]
                cap = capacity.get((u, v), 0.0)
                used = flow.get((u, v), 0.0)
                residual = cap - used
                bottleneck = min(bottleneck, residual)
                v = parent[v]

            # actualiza flujos
            v = t
            while parent[v] is not None:
                u = parent[v]
                flow[(u, v)] = flow.get((u, v), 0.0) + bottleneck
                # mantiene la entrada inversa para cálculos netos
                flow[(v, u)] = flow.get((v, u), 0.0) - bottleneck
                v = parent[v]

            max_flow += bottleneck

        return max_flow, flow

    resultados = {}
    for fuente_id, info in caminos_a_explorar.items():
        sink = info['nodo_mas_lejano']
        capacity, adj = construir_capacidades_para_sector(fuente_id)

        if not capacity or fuente_id == sink:
            resultados[fuente_id] = {
                'fuente': fuente_id,
                'nodo_mas_lejano': sink,
                'flujo_maximo': 0.0,
                'uso_tuberias': []
            }
            continue

        flujo_max, flujo_por_arista = edmonds_karp(capacity, adj, fuente_id, sink)

        uso_tuberias = []
        # Reportar uso neto por arista (undirected): tomar flow[(u,v)]
        for ar in instancia.aristas:
            par = (min(ar.nodo1, ar.nodo2), max(ar.nodo1, ar.nodo2))
            if par in aristas_cerradas:
                continue
            # Solo interesan aristas totalmente dentro del sector actual
            if asignacion_sector.get(ar.nodo1) != fuente_id or asignacion_sector.get(ar.nodo2) != fuente_id:
                continue
            net = flujo_por_arista.get((ar.nodo1, ar.nodo2), 0.0)
            uso = abs(net)
            uso_tuberias.append({
                'nodo1': ar.nodo1,
                'nodo2': ar.nodo2,
                'capacidad': ar.capacidad,
                'uso': uso
            })

        resultados[fuente_id] = {
            'fuente': fuente_id,
            'nodo_mas_lejano': sink,
            'flujo_maximo': flujo_max,
            'uso_tuberias': uso_tuberias
        }

    return resultados


def graficar_flujo_maximo_agua(instancia: Instancia, ruta_salida: str = None,
                          etapa: str = "antes") -> None:
    asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
    flujo_maximo = calcular_flujo_maximo(instancia)
    fuentes = instancia.obtener_fuentes()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    calcular_longitudes_tuberias(instancia)
    
    colores_sectores = ['#1f77b4', '#d62728', '#ff7f0e', '#2ca02c', 
                       '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    fuente_a_color = {}
    for i, fuente in enumerate(fuentes):
        fuente_a_color[fuente.id] = colores_sectores[i % len(colores_sectores)]
    
    for arista in instancia.aristas:
        par = (min(arista.nodo1, arista.nodo2),
               max(arista.nodo1, arista.nodo2))
        if par not in aristas_cerradas:
            nodo1 = instancia.nodos[arista.nodo1]
            nodo2 = instancia.nodos[arista.nodo2]
            sector = asignacion_sector[arista.nodo1]
            color = fuente_a_color.get(sector, 'gray')
            ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
                   color=color, linewidth=1.5, alpha=0.4, zorder=1)
    
    for nodo1_id, nodo2_id in aristas_cerradas:
        nodo1 = instancia.nodos[nodo1_id]
        nodo2 = instancia.nodos[nodo2_id]
        ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
               color='black', linewidth=1, linestyle='--',
               alpha=0.2, zorder=1)
    
    for fuente_id, info in flujo_maximo.items():
        color = fuente_a_color.get(fuente_id, 'gray')

        for uso_info in info['uso_tuberias']:
            nodo1 = instancia.nodos[uso_info['nodo1']]
            nodo2 = instancia.nodos[uso_info['nodo2']]
            uso = uso_info.get('uso', 0.0)
            capacidad = uso_info.get('capacidad', 0.0)
            ratio = (uso / capacidad) if capacidad > 0 else 0.0
            ancho_linea = max(0.8, min(8.0, 6 * ratio))
            ax.plot([nodo1.x, nodo2.x], [nodo1.y, nodo2.y],
                   color=color, linewidth=ancho_linea, alpha=0.8, zorder=2)
            mid_x = (nodo1.x + nodo2.x) / 2.0
            mid_y = (nodo1.y + nodo2.y) / 2.0
            etiqueta = f"{uso:.1f}/{capacidad:.1f}"
            ax.text(mid_x, mid_y, etiqueta, fontsize=7, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),
                    zorder=4)
            

    for id_nodo, nodo in instancia.nodos.items():
        sector = asignacion_sector.get(id_nodo)
        color = fuente_a_color.get(sector, 'gray')
        
        es_fuente = nodo.es_fuente
        es_mas_lejano = any(info['nodo_mas_lejano'] == id_nodo 
                           for info in flujo_maximo.values())
        
        if es_fuente:
            ax.scatter(nodo.x, nodo.y, c=color, s=500, marker='o',
                      edgecolors='black', linewidths=3, zorder=5)
        elif es_mas_lejano:
            ax.scatter(nodo.x, nodo.y, c=color, s=400, marker='s',
                      edgecolors='black', linewidths=3, zorder=5)
        else:
            ax.scatter(nodo.x, nodo.y, c=color, s=120, marker='o',
                      edgecolors='black', linewidths=1.5, zorder=4)
        
        ax.text(nodo.x, nodo.y, str(id_nodo), fontsize=8,
                ha='center', va='center', color='white',
                weight='bold', zorder=6)
    
    if instancia.office_id in instancia.nodos:
        office = instancia.nodos[instancia.office_id]
        ax.scatter(office.x, office.y, c='yellow', s=350, marker='*',
                  edgecolors='black', linewidths=2, zorder=7, label='Oficina')
    
    ax.set_xlabel('Coordenada X', fontsize=12)
    ax.set_ylabel('Coordenada Y', fontsize=12)
    
    info_flujo_maximo = '\n'.join([f"Fuente {info['fuente']} -> Nodo {info['nodo_mas_lejano']}: "
                              f"{info['flujo_maximo']:.1f} (flujo maximo)" 
                              for info in flujo_maximo.values()])
    
    titulo = (f'Flujo Maximo de Agua - {instancia.nombre}\n'
              f'{info_flujo_maximo}')
    ax.set_title(titulo, fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    
    if ruta_salida is None:
        ruta_salida = obtener_ruta_grafica(instancia, "flujo_maximo", etapa)
    
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight', format='png')
    print(f"Gráfica de flujo maximo guardada en: {ruta_salida}")
    plt.close()


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

#TODO: Completar las funciones para guardar los resultados en un archivo de texto
#Esto es por que nos pide en la linea 699
def guardar_resultados(instancia: Instancia, etapa: str = "antes",
                      directorio_base: str = "resultados") -> None:
    directorio = obtener_ruta_resultados(instancia, etapa, directorio_base)
    ruta_archivo = os.path.join(directorio, "datos.txt")
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(f"Resultados para la instancia {instancia.nombre}\n")
        f.write(f"Estado: {etapa} de agregar nodos nuevos\n\n")
        
        f.write("1. Información básica\n")
        f.write(f"La red tiene {instancia.num_nodos} nodos y {instancia.num_aristas} aristas.\n")
        f.write(f"La oficina se encuentra en el nodo {instancia.office_id}.\n")
        f.write(f"Hay {len(instancia.nuevos_nodos)} nuevos nodos pendientes de agregar.\n")
        
        fuentes = instancia.obtener_fuentes()
        f.write(f"\nSe encontraron {len(fuentes)} fuentes:\n")
        for fuente in fuentes:
            f.write(f"  Nodo {fuente.id} en ({fuente.x:.2f}, {fuente.y:.2f})\n")
        
        f.write("\n\n")
        
        f.write("2. Longitud de las tuberías\n")
        calcular_longitudes_tuberias(instancia)
        
        longitudes = [a.longitud for a in instancia.aristas 
                     if a.longitud is not None]
        if longitudes:
            total = sum(longitudes)
            promedio = total / len(longitudes)
            f.write(f"La red tiene una longitud total de {total:.2f} unidades.\n")
            f.write(f"Longitud promedio: {promedio:.2f}, mínima: {min(longitudes):.2f}, máxima: {max(longitudes):.2f}\n\n")
            
            f.write("Detalle de aristas:\n")
            for arista in instancia.aristas:
                f.write(f"  {arista.nodo1} -> {arista.nodo2}: "
                       f"{arista.longitud:.2f} unidades, "
                       f"capacidad {arista.capacidad:.1f}\n")
        
        f.write("\n\n")
        
        f.write("3. Sectorización\n")
        asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
        reporte = reportar_sectorizacion(instancia)
        
        f.write(f"La red se dividió en {reporte['num_sectores']} sectores.\n")
        f.write(f"Se cerraron {reporte['num_tuberias_cerradas']} tuberías entre sectores.\n\n")
        
        f.write("Distribución de nodos por sector:\n")
        for fuente_id, nodos in reporte['sectores'].items():
            nodos_str = ', '.join(map(str, sorted(nodos)))
            f.write(f"  Sector {fuente_id} (fuente {fuente_id}): {len(nodos)} nodos - {nodos_str}\n")
        
        if reporte['tuberias_cerradas']:
            f.write("\nTuberías cerradas:\n")
            for nodo1, nodo2 in reporte['tuberias_cerradas']:
                f.write(f"  {nodo1} - {nodo2}\n")
        
        f.write("\n\n")
        
        f.write("4. Frescura de agua\n")
        frescura = calcular_frescura_agua(instancia)
        
        for fuente_id, info in frescura.items():
            camino_str = ' -> '.join(map(str, info['camino']))
            f.write(f"\nSector de la fuente {fuente_id}:\n")
            f.write(f"  El nodo más lejano es el {info['nodo_mas_lejano']} a {info['distancia']:.2f} unidades.\n")
            f.write(f"  Camino: {camino_str}\n")
        
        f.write("\n\n")
        
        f.write("5. Flujo máximo de cada sector\n")
        flujo_maximo = calcular_flujo_maximo(instancia)

        for fuente_id, info in flujo_maximo.items():
            f.write(f"\nSector de la fuente {fuente_id}:\n")
            f.write(f"  El nodo más lejano es el {info['nodo_mas_lejano']}.\n")
            f.write(f"  Flujo máximo desde la fuente hasta el nodo más lejano: {info['flujo_maximo']:.2f} unidades.\n")
            f.write("  Uso de tuberías:\n")
            for uso_info in info['uso_tuberias']:
                f.write(f"    Tubería {uso_info['nodo1']} - {uso_info['nodo2']}: "
                       f"uso {uso_info['uso']:.2f} / capacidad {uso_info['capacidad']:.2f}\n")
       
        f.write("\n\n")

        
        f.write("6. Muestra de calidad de agua\n")
        f.write("(Pendiente de implementación)\n\n")
        
        f.write("7. Expansión de la red\n")
        f.write("(Pendiente de implementación)\n")
    
    print(f"Resultados guardados en: {ruta_archivo}")


def procesar_instancia(instancia: Instancia, etapa: str = "antes") -> None:
    graficar_red(instancia, etapa=etapa)
    graficar_sectorizacion(instancia, etapa=etapa)
    graficar_frescura_agua(instancia, etapa=etapa)
    graficar_flujo_maximo_agua(instancia, etapa=etapa)
    guardar_resultados(instancia, etapa=etapa)
    
    #TODO: Implementar lo demas


if __name__ == "__main__":
    instancias = cargar_todas_las_instancias("instancias")
    
    print(f"\nSe encontraron {len(instancias)} instancias: {', '.join(instancias.keys())}\n")
    
    for nombre, instancia in instancias.items():
        print(f"Procesando instancia: {nombre}")
        procesar_instancia(instancia, etapa="antes")
        
        # TODO: Implementar expansión de red (punto 7)
        # instancia_expandida = copiar_instancia(instancia)
        # expandir_red(instancia_expandida)
        # procesar_instancia(instancia_expandida, etapa="despues")
    