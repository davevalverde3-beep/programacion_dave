from collections import deque 

red = {
    "Santiago": ["Mercedes Sur", "Barbacoas", "Candelarita"],
    "Mercedes Sur": ["Santiago", "San Rafael"],
    "Barbacoas": ["Santiago", "Grifo Alto"],
    "San Rafael": ["Mercedes Sur", "Grifo Alto"],
    "Grifo Alto": ["Barbacoas", "San Rafael"],
    "Candelarita": ["Santiago"],
    "Desamparaditos": ["Chires"],
    "Chires": ["Desamparaditos"],
    "Zapatón": [],
}

plan = {
    "Estudio": ["Permisos", "Materiales"],
    "Permisos": ["Excavación"],
    "Materiales": ["Alcantarillado", "Asfaltado"],
    "Excavación": ["Alcantarillado"],
    "Alcantarillado": ["Asfaltado"],
    "Asfaltado": ["Señalización"],
    "Señalización": [],
}


def dfs_iterativo(grafo, inicio):
    visitados, pila = [], [inicio]

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue 
        visitados.append(actual)
        pila.extend(reversed(grafo[actual]))

    return visitados 

def ruta_mas_corta(grafo, inicio, destino):
    padres = {inicio:None}
    cola = deque([inicio])
    while cola:
        actual = cola.popleft()
        if actual == destino:
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padres[actual]
            return ruta[::-1]
        for v in grafo[actual]:
            if v not in padres:
                padres[v] = actual
                cola.append(v)

    return None
            
def contar_componentes(grafo):
    comp, n = {}, 0
    for nodo in grafo:
        if nodo in comp:
            continue
        n += 1
        comp[nodo] = n
        pila = [nodo]
        while pila:
            for v in grafo[pila.pop()]:
                if v not in comp:
                    comp[v] = n
                    pila.append(v)
    return n, comp

def tiene_ciclo(grafo):
    visitados = set()

    def visitar(nodo, padre):
        visitados.add(nodo)
        for v in grafo[nodo]:
            if v != padre and (v in visitados or visitar(v, nodo)):
                return True
        return False

    return any(visitar(n, None) for n in grafo if n not in visitados)


def orden_topologico(grafo):
    entrada = {o: 0 for o in grafo}
    for o in grafo:
        for d in grafo[o]:
            entrada[d] += 1
    cola = deque(o for o in grafo if entrada[o] == 0)
    orden = []
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for d in grafo[actual]:
            entrada[d] -= 1
            if entrada[d] == 0:
                cola.append(d)
    return orden


def pedir(*mensajes):
    return [input(m).strip().title() for m in mensajes]


def main():
    while True:
        op = input("===RED VIAL DE PURISCAL===  \n1. Ver la red de caminos" \
                "\n2.Agregar un camino \n3.Comunidades alcanzables desde un comunidad" \
                "\n4. Ruta con menos tramos entre dos comunidades \n5. Componentes conexas de la red" \
                "\n6. Detectar caminos circulares \n7. Orden de ejecucion de las obras" \
                "\n8. Agregar un prerrequisito entre las obras" \
                "\n9. Salir")


        if op == "1":
            print("\nRed de caminos de Puriscal")
            suma = 0
            for comunidad in red:
                vecinos = red[comunidad]
                suma += len(vecinos)
                if len(vecinos) == 0:
                    texto = "sin caminos"
                else:
                    texto = ", ".join(vecinos)
                print(comunidad, "(grado " + str(len(vecinos)) + "): " + texto)
            print("Total de caminos:", suma // 2)

        elif op == "2":
            a = input("Primera comunidad: ").strip().title()
            b = input("Segunda comunidad: ").strip().title()
            if a not in red or b not in red:
                print("Error: alguna comunidad no existe.")
            elif a == b:
                print("Error: son la misma comunidad.")
            elif b in red[a]:
                print("Error: el camino ya existe.")
            else:
                red[a].append(b)
                red[b].append(a)
                print("Camino agregado.")

        elif op == "3":
            inicio = input("Comunidad de inicio: ").strip().title()
            if inicio not in red:
                print("Error: la comunidad no existe.")
            else:
                visitados = dfs_iterativo(red, inicio)
                print("Comunidades alcanzables:", len(visitados))
                print(" -> ".join(visitados))

        elif op == "4":
            origen = input("Origen: ").strip().title()
            destino = input("Destino: ").strip().title()
            if origen not in red or destino not in red:
                print("Error: alguna comunidad no existe.")
            elif origen == destino:
                print("Error: origen y destino son iguales.")
            else:
                ruta = ruta_mas_corta(red, origen, destino)
                if ruta is None:
                    print("Las comunidades no están comunicadas.")
                else:
                    print(" -> ".join(ruta))
                    print("Tramos:", len(ruta) - 1)

        elif op == "5":
            cantidad, componentes = contar_componentes(red)
            for numero in range(1, cantidad + 1):
                miembros = []
                for comunidad in red:
                    if componentes[comunidad] == numero:
                        miembros.append(comunidad)
                print("Componente " + str(numero) + ": " + ", ".join(miembros))
            print("Total de componentes:", cantidad)
            if cantidad == 1:
                print("Todas las comunidades están comunicadas.")
            else:
                print("No todas las comunidades están comunicadas.")

        elif op == "6":
            hay_ciclo = tiene_ciclo(red)
            cantidad, componentes = contar_componentes(red)
            suma = 0
            for comunidad in red:
                suma += len(red[comunidad])
            caminos = suma // 2
            esperados = len(red) - cantidad
            por_conteo = caminos > esperados
            print("Recorrido en profundidad - hay ciclo:", hay_ciclo)
            print("Conteo (caminos:", caminos, "- esperados sin ciclos:", esperados, ") - hay ciclo:", por_conteo)
            if hay_ciclo == por_conteo:
                print("Ambos métodos coinciden.")
            else:
                print("Los métodos no coinciden.")

        elif op == "7":
            orden = orden_topologico(plan)
            if len(orden) == len(plan):
                print(" -> ".join(orden))
            else:
                print("Existe un ciclo de prerrequisitos.")
                bloqueadas = []
                for obra in plan:
                    if obra not in orden:
                        bloqueadas.append(obra)
                print("Obras bloqueadas:", ", ".join(bloqueadas))

        elif op == "8":
            previa = input("Obra previa: ").strip().title()
            dependiente = input("Obra que depende de ella: ").strip().title()
            if previa not in plan or dependiente not in plan:
                print("Error: alguna obra no existe.")
            elif previa == dependiente:
                print("Error: son la misma obra.")
            elif dependiente in plan[previa]:
                print("Error: la dependencia ya existe.")
            else:
                plan[previa].append(dependiente)
                print("Prerrequisito agregado.")

        elif op == "9":
            print("Chao")
            break

        else:
            print("Error opcion no valida")

main()