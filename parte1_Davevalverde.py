grafo[ciudad]=[]

def agregar_ruta(grafo, a, b):
    grafo[a].append(b)
    grafo[b].append(a)

def rutas_directas(grafo, ciudad):
    return sorted(grafo[ciudad])

def se_puede_llegar(grafo, origen,destino): 
    visitados = set()
    return dfs(grafo, origen, destino, visitados)

def minimo_trayectos (grafo, origen, destino):
    visitados = set()
    return bfs(grafo, origen, destino,visitados)

def contar_zonas(grafo):
    visitados = set()
    zonas = 0
    for ciudad in grafo:
        if ciudad not in visitados:
            dfs(grafo, ciudad, None, visitados)
            zonas += 1
    return zonas

def main():
     
    grafo = {}

    agregar_ruta(grafo,"San Jose","atenas")
    agregar_ruta(grafo,"San Jose","puriscal")
    agregar_ruta(grafo,"San Jose","orotina")
    agregar_ruta(grafo,"atenas","orotina")
    agregar_ruta(grafo,"orotina","jaco")
    agregar_ruta(grafo,"puriscal","parrita")
    agregar_ruta(grafo,"cartago","turrialba")

    while True:
        op = input("===RED DE BUSES===\n1. Consultar rutas directas" \
        "\n2.verificar si se puede llegar\n3.calcular minimos de tayectos" \
        "\n4. Contar zonas sin conexión\n5. agregar ruta\n6. salir ")

        if op == "1":
            ciudad = input("Ingrese la ciudad: ")
            if ciudad in grafo:
                rutas = rutas_directas(grafo, ciudad)
                print(f"Rutas directas desde {ciudad}: {', '.join(rutas)}")

        if op == "2":
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            if origen in grafo and destino in grafo:
                if se_puede_llegar(grafo, origen, destino):
                    print("si")
                else:
                    print("no")

        if op == "3":
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            if origen in grafo and destino in grafo:
                trayectos = minimo_trayectos(grafo, origen, destino)
                print(f"Trayectos mínimos: {trayectos}")

            else:
                print(f"no existe ruta entre {origen} y {destino}")

        if op == "4":
            zonas = contar_zonas(grafo)
            print(f"Zonas sin conexión: {zonas}")

        if op == "5":
            ciudad1 = input("Ingrese la primera ciudad: ")
            ciudad2 = input("Ingrese la segunda ciudad: ")
            agregar_ruta(grafo, ciudad1, ciudad2)

        if op == "6":
            break

main()
