#!/usr/bin/env python3
"""
Test completo del sistema de distribución de agua.
Verifica todas las funcionalidades implementadas.
"""

from Distribucion_del_Agua import (
    cargar_todas_las_instancias,
    calcular_longitudes_tuberias,
    sectorizar_red,
    reportar_sectorizacion,
    calcular_frescura_agua,
    graficar_red,
    graficar_sectorizacion,
    graficar_frescura_agua
)

def test_carga_instancias():
    """Test 1: Verificar carga de instancias"""
    print("=" * 70)
    print("TEST 1: Carga de Instancias")
    print("=" * 70)
    
    instancias = cargar_todas_las_instancias("instancias")
    
    assert len(instancias) > 0, "No se cargaron instancias"
    print(f"✓ Se cargaron {len(instancias)} instancias")
    
    for nombre, instancia in instancias.items():
        assert instancia.num_nodos == len(instancia.nodos), \
            f"Error en {nombre}: nodos esperados vs cargados"
        assert instancia.num_aristas == len(instancia.aristas), \
            f"Error en {nombre}: aristas esperadas vs cargadas"
        assert instancia.office_id in instancia.nodos, \
            f"Error en {nombre}: office_id no válido"
        
        fuentes = instancia.obtener_fuentes()
        assert len(fuentes) > 0, f"Error en {nombre}: no hay fuentes"
        
        print(f"  ✓ {nombre}: {instancia.num_nodos} nodos, "
              f"{instancia.num_aristas} aristas, "
              f"{len(fuentes)} fuentes, "
              f"{len(instancia.nuevos_nodos)} nuevos nodos")
    
    print("✓ TEST 1 PASADO\n")
    return instancias


def test_longitudes_tuberias(instancias):
    """Test 2: Verificar cálculo de longitudes"""
    print("=" * 70)
    print("TEST 2: Cálculo de Longitudes de Tuberías")
    print("=" * 70)
    
    for nombre, instancia in instancias.items():
        calcular_longitudes_tuberias(instancia)
        
        longitudes_calculadas = sum(1 for a in instancia.aristas 
                                   if a.longitud is not None)
        assert longitudes_calculadas == len(instancia.aristas), \
            f"Error en {nombre}: no todas las longitudes fueron calculadas"
        
        longitudes = [a.longitud for a in instancia.aristas 
                     if a.longitud is not None]
        assert all(l > 0 for l in longitudes), \
            f"Error en {nombre}: hay longitudes inválidas"
        
        total = sum(longitudes)
        promedio = total / len(longitudes) if longitudes else 0
        
        print(f"  ✓ {nombre}: Todas las longitudes calculadas")
        print(f"    Total: {total:.2f}, Promedio: {promedio:.2f}, "
              f"Mín: {min(longitudes):.2f}, Máx: {max(longitudes):.2f}")
    
    print("✓ TEST 2 PASADO\n")


def test_sectorizacion(instancias):
    """Test 3: Verificar sectorización"""
    print("=" * 70)
    print("TEST 3: Sectorización")
    print("=" * 70)
    
    for nombre, instancia in instancias.items():
        asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
        
        assert len(asignacion_sector) == len(instancia.nodos), \
            f"Error en {nombre}: no todos los nodos tienen sector asignado"
        
        fuentes = instancia.obtener_fuentes()
        sectores_unicos = set(asignacion_sector.values())
        assert len(sectores_unicos) == len(fuentes), \
            f"Error en {nombre}: número de sectores incorrecto"
        
        for nodo_id, fuente_id in asignacion_sector.items():
            assert fuente_id in [f.id for f in fuentes], \
                f"Error en {nombre}: sector asignado no es una fuente válida"
        
        reporte = reportar_sectorizacion(instancia)
        assert reporte['num_sectores'] == len(fuentes), \
            f"Error en {nombre}: número de sectores en reporte incorrecto"
        
        print(f"  ✓ {nombre}: {len(fuentes)} sectores, "
              f"{len(aristas_cerradas)} tuberías cerradas")
        for fuente_id, nodos in reporte['sectores'].items():
            print(f"    Sector {fuente_id}: {len(nodos)} nodos")
    
    print("✓ TEST 3 PASADO\n")


def test_frescura_agua(instancias):
    """Test 4: Verificar frescura de agua"""
    print("=" * 70)
    print("TEST 4: Frescura de Agua")
    print("=" * 70)
    
    for nombre, instancia in instancias.items():
        frescura = calcular_frescura_agua(instancia)
        
        fuentes = instancia.obtener_fuentes()
        assert len(frescura) == len(fuentes), \
            f"Error en {nombre}: no se calculó frescura para todas las fuentes"
        
        for fuente_id, info in frescura.items():
            assert info['fuente'] == fuente_id, \
                f"Error en {nombre}: fuente_id inconsistente"
            assert info['nodo_mas_lejano'] in instancia.nodos, \
                f"Error en {nombre}: nodo más lejano no válido"
            assert info['distancia'] > 0, \
                f"Error en {nombre}: distancia inválida"
            assert len(info['camino']) > 0, \
                f"Error en {nombre}: camino vacío"
            assert info['camino'][0] == fuente_id, \
                f"Error en {nombre}: camino no inicia en la fuente"
            assert info['camino'][-1] == info['nodo_mas_lejano'], \
                f"Error en {nombre}: camino no termina en nodo más lejano"
        
        print(f"  ✓ {nombre}: Frescura calculada para {len(frescura)} sectores")
        for fuente_id, info in frescura.items():
            print(f"    Fuente {fuente_id} -> Nodo {info['nodo_mas_lejano']}: "
                  f"{info['distancia']:.1f} (camino: {len(info['camino'])} nodos)")
    
    print("✓ TEST 4 PASADO\n")


def test_graficas(instancias):
    """Test 5: Verificar generación de gráficas"""
    print("=" * 70)
    print("TEST 5: Generación de Gráficas")
    print("=" * 70)
    
    import os
    
    for nombre, instancia in instancias.items():
        # Test gráfica de red
        ruta_red = f"instancias/{nombre}_test_red.png"
        graficar_red(instancia, ruta_red, mostrar_etiquetas=False)
        assert os.path.exists(ruta_red), \
            f"Error en {nombre}: gráfica de red no generada"
        print(f"  ✓ {nombre}: Gráfica de red generada")
        
        # Test gráfica de sectorización
        ruta_sector = f"instancias/{nombre}_test_sectorizacion.png"
        graficar_sectorizacion(instancia, ruta_sector)
        assert os.path.exists(ruta_sector), \
            f"Error en {nombre}: gráfica de sectorización no generada"
        print(f"  ✓ {nombre}: Gráfica de sectorización generada")
        
        # Test gráfica de frescura
        ruta_frescura = f"instancias/{nombre}_test_frescura.png"
        graficar_frescura_agua(instancia, ruta_frescura)
        assert os.path.exists(ruta_frescura), \
            f"Error en {nombre}: gráfica de frescura no generada"
        print(f"  ✓ {nombre}: Gráfica de frescura generada")
    
    print("✓ TEST 5 PASADO\n")


def test_integracion(instancias):
    """Test 6: Test de integración completo"""
    print("=" * 70)
    print("TEST 6: Test de Integración Completo")
    print("=" * 70)
    
    for nombre, instancia in instancias.items():
        # Flujo completo
        calcular_longitudes_tuberias(instancia)
        asignacion_sector, aristas_cerradas = sectorizar_red(instancia)
        frescura = calcular_frescura_agua(instancia)
        
        # Verificar consistencia
        fuentes = instancia.obtener_fuentes()
        assert len(frescura) == len(fuentes), \
            f"Error en {nombre}: inconsistencia entre fuentes y frescura"
        
        # Verificar que los caminos de frescura no usan tuberías cerradas
        for fuente_id, info in frescura.items():
            camino = info['camino']
            for i in range(len(camino) - 1):
                par = (min(camino[i], camino[i+1]),
                      max(camino[i], camino[i+1]))
                assert par not in aristas_cerradas, \
                    f"Error en {nombre}: camino usa tubería cerrada"
        
        print(f"  ✓ {nombre}: Integración completa exitosa")
        print(f"    - Longitudes: ✓")
        print(f"    - Sectorización: {len(fuentes)} sectores, "
              f"{len(aristas_cerradas)} cerradas")
        print(f"    - Frescura: {len(frescura)} caminos calculados")
    
    print("✓ TEST 6 PASADO\n")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 70)
    print("SUITE DE TESTS - Sistema de Distribución de Agua")
    print("=" * 70 + "\n")
    
    try:
        # Test 1: Carga
        instancias = test_carga_instancias()
        
        # Test 2: Longitudes
        test_longitudes_tuberias(instancias)
        
        # Test 3: Sectorización
        test_sectorizacion(instancias)
        
        # Test 4: Frescura
        test_frescura_agua(instancias)
        
        # Test 5: Gráficas
        test_graficas(instancias)
        
        # Test 6: Integración
        test_integracion(instancias)
        
        print("=" * 70)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 70)
        print("\nResumen:")
        print(f"  - Instancias probadas: {len(instancias)}")
        print(f"  - Tests ejecutados: 6")
        print(f"  - Estado: TODO FUNCIONANDO CORRECTAMENTE")
        print()
        
    except AssertionError as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

