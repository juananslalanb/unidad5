# Explorador CLI para el Analisis y Visualizacion de Archivos Reales
# Modulos usados: os (solo para listar archivos), pathlib, csv y matplotlib

import os
import csv
from pathlib import Path
import matplotlib.pyplot as plt

# Palabras que no utilizamos, conectores en español y ingles 
CONECTORES = ["el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
              "y", "o", "a", "en", "que", "se", "por", "con", "para", "es", "al",
              "lo", "su", "sus", "como", "mas", "pero", "sin", "me", "mi", "te",
              "tu", "si", "no", "ha", "le", "the", "and", "of", "to", "in", "is",
              "it", "that", "was", "for", "on", "with", "as", "he", "she", "his",
              "her", "at", "by", "be", "this", "had", "not", "are", "but", "from",
              "or", "have", "an", "they", "which", "you", "were", "i", "my","yo","él","más","porque","ni","tan"]

# Signos que se quitan a las palabras
SIGNOS = ".,;:!?\"'()[]{}-_*#"
# FUNCIONES
def pedir_numero(texto, minimo, maximo):
    while True:
        dato = input(texto)
        try:
            numero = int(dato)
            if numero >= minimo and numero <= maximo:
                return numero
            print("Escribe un numero entre", minimo, "y", maximo)
        except ValueError:
            print("Eso no es un numero valido.")
def a_numero(texto):
 #Convierte texto a numero. Si no se puede (vacio, 'NA', 'nan'...)
    #devuelve None.
    try:
        n = float(texto.replace(",", "."))   
    except ValueError:
        return None
    if n != n:                               
        return None
    if n == float("inf") or n == float("-inf"):
        return None
    return n


def elegir_columna(encabezados, mensaje):
    #Muestra las columnas y devuelve la posicion elegida.
    print("\nColumnas disponibles:")
    for i in range(len(encabezados)):
        print(" ", i + 1, ".", encabezados[i])
    return pedir_numero(mensaje, 1, len(encabezados)) - 1


def top_n(conteo, n):
    #Recibe un diccionario  y los vuelve dos listas 
    claves = []
    cantidades = []
    for c in conteo:
        claves.append(c)
        cantidades.append(conteo[c])

    res_claves = []
    res_cantidades = []
    for i in range(n):
        if len(claves) == 0:
            break
        mejor = 0
        for j in range(len(claves)):
            if cantidades[j] > cantidades[mejor]:
                mejor = j
        res_claves.append(claves[mejor])
        res_cantidades.append(cantidades[mejor])
        claves.pop(mejor)
        cantidades.pop(mejor)
    return res_claves, res_cantidades

# PROGRAMA PRINCIPAL

# Carpeta donde se buscan los archivos: por defecto, la del programa
try:
    carpeta_actual = Path(__file__).parent
except NameError:
    carpeta_actual = Path(".")

while True:
    print("EXPLORADOR CLI \n Carpeta actual:", carpeta_actual.resolve()," \n 1. Explorar directorio"," \n 2. Procesar bitacoras / textos reales (.txt) \n 3. Analizar dataset de datos abiertos (.csv) \n 4. Salir")
    opcion = pedir_numero("Elige una opcion: ", 1, 4)

    # 1. EXPLORAR DIRECTORIO
    if opcion == 1:
        texto_ruta = input("Ruta de la carpeta (Enter para la actual): ")
        if texto_ruta == "":
            ruta = carpeta_actual
        else:
            ruta = Path(texto_ruta)

        if not ruta.exists():
            print("La carpeta no existe:", ruta)
        else:
            try:
                archivos = os.listdir(ruta)
                carpeta_actual = ruta        # la recordamos para las otras opciones
                print("\nArchivos .txt y .csv en", ruta.resolve(), ":")
                encontrados = 0
                for nombre in archivos:
                    minuscula = nombre.lower()
                    if minuscula.endswith(".txt") or minuscula.endswith(".csv"):
                        print(" -", nombre)
                        encontrados = encontrados + 1
                if encontrados == 0:
                    print("(No hay archivos .txt ni .csv en esta carpeta)")
                    print("Revisa la ruta y que los archivos no tengan doble extension")
                    print("(por ejemplo datos.csv.txt).")
            except OSError:
                print("No se pudo leer esa ruta (debe ser una carpeta y tener permiso).")

    # 2. PROCESAR TEXTOS (.txt)
    elif opcion == 2:
        nombre = input("Nombre del archivo (.txt): ")
        if not nombre.lower().endswith(".txt"):
            print("El archivo debe terminar en .txt")
            continue

        ruta = carpeta_actual / nombre
        try:
            with open(ruta, "r", encoding="utf-8-sig", errors="ignore") as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print("No se encontro el archivo:", ruta.resolve())
            print("Usa la opcion 1 para ver que archivos hay en la carpeta.")
            continue
        except OSError:
            print("No se pudo leer el archivo.")
            continue

        if len(lineas) == 0:
            print("El archivo esta vacio.")
            continue

        # Se calcula todo una sola vez al abrir el archivo
        total_palabras = 0
        chars_con_espacios = 0
        chars_sin_espacios = 0
        longitudes = []
        conteo = {}
        for linea in lineas:
            linea = linea.rstrip("\r\n")         # quitamos el salto de linea
            palabras = linea.split()
            total_palabras = total_palabras + len(palabras)
            chars_con_espacios = chars_con_espacios + len(linea)
            chars_sin_espacios = chars_sin_espacios + len("".join(palabras))
            longitudes.append(len(linea))

            for palabra in palabras:
                palabra = palabra.lower().strip(SIGNOS)
                if len(palabra) < 2 or palabra in CONECTORES:
                    continue
                if palabra in conteo:
                    conteo[palabra] = conteo[palabra] + 1
                else:
                    conteo[palabra] = 1

        while True:
            print("\n PROCESAR TEXTO (.txt)  \n 1. Resumen estadistico del texto \n 2. Extraccion de patrones (logs)\n 3. Grafico 1 - Frecuencia de palabras \n 4. Grafico 2 - Distribucion de longitud de lineas \n 5. Volver al menu principal")
            opc = pedir_numero("Elige una opcion: ", 1, 5)

            if opc == 1:
                print("\n--- RESUMEN DEL TEXTO --- \n Total de lineas:, len(lineas) \n Total de palabras:", total_palabras," \n Caracteres (con espacios):", chars_con_espacios, " \n Caracteres (sin espacios):", chars_sin_espacios, "\nTop 5 palabras mas repetidas (sin conectores):")
                claves, cantidades = top_n(conteo, 5)
                for i in range(len(claves)):
                    print(" ", i + 1, ".", claves[i], "->", cantidades[i], "veces")

            elif opc == 2:
                print("\nEXTRACCION DE PATRONES")
                patrones = ["ERROR", "WARNING", "404", "500"]
                otro = input("Escribe una fecha o texto a buscar (Enter para omitir): ")
                if otro != "":
                    patrones.append(otro)
                for patron in patrones:
                    cantidad = 0
                    for linea in lineas:
                        if patron in linea:
                            cantidad = cantidad + 1
                    print("Lineas con '" + patron + "':", cantidad)

            elif opc == 3:
                claves, cantidades = top_n(conteo, 10)
                if len(claves) == 0:
                    print("No hay palabras para graficar.")
                else:
                    # Al reves para que la mas frecuente quede arriba en barh
                    palabras_g = []
                    cantidades_g = []
                    for i in range(len(claves) - 1, -1, -1):
                        palabras_g.append(claves[i])
                        cantidades_g.append(cantidades[i])

                    plt.figure()
                    plt.barh(palabras_g, cantidades_g)
                    plt.title("Las 10 palabras mas frecuentes")
                    plt.xlabel("Cantidad de apariciones")
                    plt.ylabel("Palabra")
                    plt.show()

            elif opc == 4:
                maxima = max(longitudes)

                # Grupos: 0-50, 51-100, 101-150...
                # Los cortes van en -0.5, 50.5, 100.5... para que una linea de
                # exactamente 50 caracteres quede en el grupo 0-50.
                cortes = [-0.5]
                corte = 50.5
                while corte < maxima + 50:
                    cortes.append(corte)
                    corte = corte + 50

                # Etiquetas del eje X ("0-50", "51-100"...), centradas en cada barra
                total_grupos = len(cortes) - 1
                paso = total_grupos // 10
                if paso < 1:
                    paso = 1
                pos_ticks = []
                texto_ticks = []
                for i in range(0, total_grupos, paso):
                    pos_ticks.append((cortes[i] + cortes[i + 1]) / 2)
                    if i == 0:
                        texto_ticks.append("0-50")
                    else:
                        texto_ticks.append(str(i * 50 + 1) + "-" + str((i + 1) * 50))

                plt.figure()
                plt.hist(longitudes, bins=cortes, edgecolor="black")
                plt.xticks(pos_ticks, texto_ticks, rotation=45)
                plt.title("Distribucion de la longitud de las lineas")
                plt.xlabel("Caracteres por linea (grupos de 50)")
                plt.ylabel("Cantidad de lineas")
                plt.tight_layout()
                plt.show()

            else:
                break
    # 3. ANALIZAR DATASET (.csv)
    elif opcion == 3:
        nombre = input("Nombre del archivo (.csv): ")
        if not nombre.lower().endswith(".csv"):
            print("El archivo debe terminar en .csv")
            continue

        ruta = carpeta_actual / nombre
        try:
            with open(ruta, "r",) as archivo:
                primera = archivo.readline()
            if primera.strip() == "":
                print("El archivo esta vacio.")
                continue
            separador = ","
            if primera.count(";") > primera.count(","):
                separador = ";"

            # Ahora se lee todo con csv.reader
            filas = []
            with open(ruta, "r") as archivo:
                lector = csv.reader(archivo, delimiter=separador)
                encabezados = next(lector)       # la primera fila son los encabezados
                for fila in lector:
                    if len(fila) > 0:            # saltamos lineas vacias
                        filas.append(fila)
        except FileNotFoundError:
            print("No se encontro el archivo:", ruta.resolve())
            print("Usa la opcion 1 para ver que archivos hay en la carpeta.")
            continue
        except OSError:
            print("No se pudo leer el archivo.")
            continue

        if len(filas) == 0:
            print("El archivo no tiene filas de datos.")
            continue

        while True:
            print("\nANALIZAR DATASET (.csv) \n 1. Vista previa de datos \n 2. Estadisticas descriptivas \n 3. Grafico 3 - Evolucion / tendencia (lineas) \n 4. Grafico 4 - Comparacion categorica (pastel) \n 5. Grafico 5 - Correlacion (dispersion) \n 6. Volver al menu principal")
            opc = pedir_numero("Elige una opcion: ", 1, 6)
            if opc == 1:
                print("\nPRIMERAS 10 FILAS ")
                print(encabezados)
                limite = 10
                if len(filas) < 10:
                    limite = len(filas)
                for i in range(limite):
                    print(filas[i])

                print("\nULTIMAS 5 FILAS")
                print(encabezados)
                inicio = len(filas) - 5
                if inicio < 0:
                    inicio = 0
                for i in range(inicio, len(filas)):
                    print(filas[i])

            elif opc == 2:
                col = elegir_columna(encabezados, "Elige la columna numerica: ")

                numeros = []
                for fila in filas:
                    if col < len(fila):
                        n = a_numero(fila[col])
                        if n is not None:        # no se ponen ni nulos ni vacios
                            numeros.append(n)

                if len(numeros) == 0:
                    print("Esa columna no tiene numeros validos.")
                else:
                    total = len(numeros)
                    promedio = sum(numeros) / total
                    maximo = max(numeros)
                    minimo = min(numeros)

                    medio = total // 2
                    ordenados = []
                    while len(ordenados) <= medio:
                        menor = min(numeros)
                        ordenados.append(menor)
                        numeros.remove(menor)
                    if total % 2 == 1:
                        mediana = ordenados[medio]
                    else:
                        mediana = (ordenados[medio - 1] + ordenados[medio]) / 2

                    print("\n--- ESTADISTICAS DE '" + encabezados[col] + "' ---, \n Registros validos: ", total," \n Registros descartados (vacios/invalidos):", (len(filas) - total)," \n Promedio:", round(promedio, 2)," \n Mediana:", mediana," \n Maximo:", maximo," \n Minimo:", minimo)
            elif opc == 3:
                print("\nColumna del eje X (ej. fecha):")
                col_x = elegir_columna(encabezados, "Columna X: ")
                print("\nColumna del eje Y (numerica):")
                col_y = elegir_columna(encabezados, "Columna Y: ")

                etiquetas = []
                valores_y = []
                for fila in filas:
                    if col_x < len(fila) and col_y < len(fila):
                        y = a_numero(fila[col_y])
                        if y is not None:
                            etiquetas.append(fila[col_x])
                            valores_y.append(y)

                if len(valores_y) == 0:
                    print("No hay datos numericos validos en la columna Y.")
                else:
                    posiciones = []
                    for i in range(len(valores_y)):
                        posiciones.append(i)

                    paso = len(valores_y) // 10
                    if paso < 1:
                        paso = 1
                    pos_ticks = []
                    texto_ticks = []
                    for i in range(0, len(valores_y), paso):
                        pos_ticks.append(i)
                        texto_ticks.append(etiquetas[i])

                    plt.figure()
                    plt.plot(posiciones, valores_y)
                    plt.xticks(pos_ticks, texto_ticks, rotation=45)
                    plt.title(encabezados[col_y] + " vs " + encabezados[col_x])
                    plt.xlabel(encabezados[col_x])
                    plt.ylabel(encabezados[col_y])
                    plt.show()

            elif opc == 4:
                col = elegir_columna(encabezados, "Elige la columna categorica: ")

                conteo_cat = {}
                total = 0
                for fila in filas:
                    if col < len(fila) and fila[col] != "":
                        categoria = fila[col]
                        if categoria in conteo_cat:
                            conteo_cat[categoria] += 1
                        else:
                            conteo_cat[categoria] = 1
                        total += 1

                if total == 0:
                    print("Esa columna no tiene datos.")
                else:
                    nombres, cantidades = top_n(conteo_cat, 8) # Las 8 categorias mas grandes; el resto se agrupa en "Otros"
                    resto = total - sum(cantidades)
                    if resto > 0:
                        nombres.append("Otros")
                        cantidades.append(resto)

                    plt.figure()
                    plt.pie(cantidades, labels=nombres, autopct="%1.1f%%")
                    plt.title("Participacion por " + encabezados[col])
                    plt.show()

            elif opc == 5:
                print("\nPrimera columna numerica (eje X):")
                col_x = elegir_columna(encabezados, "Columna X: ")
                print("\nSegunda columna numerica (eje Y):")
                col_y = elegir_columna(encabezados, "Columna Y: ")

                xs = []
                ys = []
                for fila in filas:
                    if col_x < len(fila) and col_y < len(fila):
                        x = a_numero(fila[col_x])
                        y = a_numero(fila[col_y])
                        if x is not None and y is not None:   # ambos deben servir
                            xs.append(x)
                            ys.append(y)

                if len(xs) == 0:
                    print("No hay pares de datos numericos validos.")
                else:
                    plt.figure()
                    plt.scatter(xs, ys)
                    plt.title("Relacion entre " + encabezados[col_x] + " y " + encabezados[col_y])
                    plt.xlabel(encabezados[col_x])
                    plt.ylabel(encabezados[col_y])
                    plt.show()

            else:
                break

    # 4. SALIR
    else:
        print("adios henry")
        break