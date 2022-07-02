import sys
import marshal
import requests
import os
import shutil

url_pokapi = 'https://pokeapi.co/api/v2/pokemon/'

class pokemones():
    dia_nacimiento = ''
    mes_nacimiento = ''
    year_nacimiento = ''
    comida_favorit = ''
    tipo_sangre = ''
    latitud = ''
    longitud = ''
    nombre_poke = ''
    lista_type_pokemons = ''
    sprites = ''

list_pokemons = []

try:
    fileIN = open("datos.dat", "br")
    deserialized = marshal.load(fileIN)
    for n in deserialized:
        pok = pokemones()
        pok.dia_nacimiento = n[0]
        pok.mes_nacimiento = n[1]
        pok.year_nacimiento = n[2]
        pok.comida_favorit = n[3]
        pok.tipo_sangre = n[4]
        pok.latitud = n[5]
        pok.longitud = n[6]
        pok.nombre_poke = n[7]
        pok.lista_type_pokemons = n[8]
        pok.sprites = n[9]
        list_pokemons.append(pok)
    print('\n================================================')
    print('=   Se encontraron',len(list_pokemons),'pokemon(es).             =')
    print('================================================')
    fileIN.close()
except:
    print('\nDatos no encontrados.\n')

def menu():
    print('\n================================================')
    print('=      MENU PARA EL PROGRAMA DE POKEMONES      =')
    print('================================================')
    print('=                                              =')
    print('=        1 ─ Agregar pokemones                 =')
    print('=        2 ─ Ver Pokemones                     =')
    print('=        3 ─ Reportes                          =')
    print('=        4 ─ Exportar Pokemon                  =')
    print('=        5 ─ Exportar Mapa                     =')
    print('=        6 ─ Salir                             =')
    print('=                                              =')
    print('================================================')

    answer = input('¿Amante a los pokemones que deseas hacer? |>> ')

    if answer == '1':
        addPokemons()
    elif answer == '2':
        seePokemons()
    elif answer == '3':
        reportPokemons()
    elif answer == '4':
        exportPokemons()
    elif answer == '5':
        exportMapPokemons()
    elif answer == '6':
        list_datos_ext = []
        for n in list_pokemons:
            list_intern = []
            list_intern.append(n.dia_nacimiento)
            list_intern.append(n.mes_nacimiento)
            list_intern.append(n.year_nacimiento)
            list_intern.append(n.comida_favorit)
            list_intern.append(n.tipo_sangre)
            list_intern.append(n.latitud)
            list_intern.append(n.longitud)
            list_intern.append(n.nombre_poke)
            list_intern.append(n.lista_type_pokemons)
            list_intern.append(n.sprites)
            list_datos_ext.append(list_intern)
        fileWRT = open("datos.dat", "bw")
        marshal.dump(list_datos_ext, fileWRT)
        fileWRT.close()
        os.system('cls')
        print('================================================')
        print('=         Se ha cerrado exitosamente.          =')
        print('================================================')
        sys.exit()
    else:
        os.system('cls')
        print('\n=================ERROR==========================')
        print('=    Valor inválido, inténtelo nuevamente.     =')
        print('=================ERROR==========================\n')
        menu()

def addPokemons():
    print('================================================')
    print('==============AGREGUE UN POKEMON================')
    print('================================================')
    pok = pokemones()
    pok.nombre_poke = input('\nNombre del pokemon: \n')

    datos_pokemons_link = url_pokapi + pok.nombre_poke
    print('Verificando, espere...')
    datos_pokemons = obtener_datos_pokemons(datos_pokemons_link)
    if not datos_pokemons:
        print('\n=================ERROR==========================')
        print('===ERROR: El nombre del pokemon es inválido.====')
        print('=================ERROR==========================\n')
        addPokemons()

    pok.lista_type_pokemons = [pokemon_tipo['type']['name'] for pokemon_tipo in datos_pokemons['types']]
    pok.sprites = datos_pokemons['sprites']

    try:
        pok.dia_nacimiento = int(input('•Dia de nacimiento: '))
        pok.mes_nacimiento = int(input('•Mes de nacimiento: '))
        pok.year_nacimiento = int(input('•Año de nacimiento: '))
        pok.comida_favorit = input('•Comida favorita: ').capitalize()
        pok.tipo_sangre = input('•Tipo de sangre: ').capitalize()
        pok.latitud = float(input('•Latitud (Capturado): '))
        pok.longitud = float(input('•Longitud (Capturado): '))
        list_pokemons.append(pok)
    except:
        print('Valor inválido, intentelo de nuevo.')
        addPokemons()

    try:
        os.system('cls')
    except:
        os.system('clear')
    print('\n================================================')
    print('=========POKEMON AGREGADO EXITOSAMENTE==========')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def seePokemons():
    try:
        os.system('cls')
    except:
        os.system('clear')
    cant_pokemones = len(list_pokemons)
    print(f'\n========HAY {cant_pokemones} POKEMON(ES) AGREGADO(S)=========\n')
    print('█ Nombre \t█ Fecha-Nacimiento(Dia/Mes/Año) █ Tipo-Sangre █ Signo-Zodiacal █ Tipos █\n')
    for n in list_pokemons:
        sig = sig_zod(n.dia_nacimiento, n.mes_nacimiento)
        print(f'█ {n.nombre_poke}\t█ {n.dia_nacimiento}/{n.mes_nacimiento}/{n.year_nacimiento} \t█ {n.tipo_sangre}\t █ {sig} █',', '.join(n.lista_type_pokemons),' █')
    print('================================================')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def reportPokemons():
    try:
        os.system('cls')
    except:
        os.system('clear')
    print('\n================================================')
    print('=                 REPORTES                     =')
    print('================================================')
    print('=                                              =')
    print('=        a ) ─ Cumpleaños por mes.             =')
    print('=        b ) ─ Pokemones por tipo.             =')
    print('=        c ) ─ Comida por tipo.                =')
    print('=                                              =')
    print('================================================')

    response = str(input('¿Que reporte deseas hacer? |>> ')).upper()

    if response == 'A':
        reportPorMes()
    elif response == 'B':
        reportPorTipos()
    elif response == 'C':
        reportComidaPorTipo()
    else:
        try:
            os.system('cls')
        except:
            os.system('clear')
        menu()

def reportPorMes():
    try:
        os.system('cls')
    except:
        os.system('clear')
    print('================================================')
    print('==============CUMPLEAÑOS POR MES================')
    print('============MESES EN NUMEROS ─ 1-12=============')
    print('================================================')

    while True:
        try:
            mes = int(input('¿Por qué mes deseas hacer el reporte de cumpleaños? '))
            break
        except:
            print('===Valor invalido intentelo nuevamente===')

    print('\n')

    lista_pokmn_por_mes = []

    for n in list_pokemons:
        if mes == int(n.mes_nacimiento):
            lista_pokmn_por_mes.append(n)
            sig = sig_zod(n.dia_nacimiento, n.mes_nacimiento)
            print(f'█ {n.nombre_poke}\t█ {n.dia_nacimiento}/{n.mes_nacimiento}/{n.year_nacimiento} \t█ {n.tipo_sangre}\t █ {sig} █',', '.join(n.lista_type_pokemons),' █')

    print('\n================================================')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def reportPorTipos():
    try:
        os.system('cls')
    except:
        os.system('clear')
    print('================================================')
    print('==============POKEMONES POR TIPO================')
    print('================================================')
    print('\n')

    lista_cant_tipos = []
    lista_type_cant_duplicate = []

    for n in list_pokemons:
        for i in n.lista_type_pokemons:
            lista_cant_tipos.append(i)

    for x in lista_cant_tipos:
        if x == x:
            contar = lista_cant_tipos.count(x)
            test = f'\t█ {x}: {contar}'
            lista_type_cant_duplicate.append(test)

    del_duplicate = sorted(list(set(lista_type_cant_duplicate)))
    juntar_tipos ='\n'.join(del_duplicate)
    print(juntar_tipos)

    print('\n================================================')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def reportComidaPorTipo():
    try:
        os.system('cls')
    except:
        os.system('clear')
    print('================================================')
    print('==========COMIDA POR TIPO DE POKEMON============')
    print('================================================\n')

    lista_tipo_Y_comida = []

    for n in list_pokemons:
        for i in n.lista_type_pokemons:
            lista_tipo_Y_comida.append({i: n.comida_favorit})

    dic = {}
    for n in lista_tipo_Y_comida:
        for i,t in n.items():
            if dic.get(i):
                dic[i] += ', '+t
            else:
                dic[i] = t

    for i,t in dic.items():
        print(f'\t█ {i}: {t}')

    print('\n================================================')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def exportPokemons():
    try:
        os.system('cls')
    except:
        os.system('clear')
    cant_pokemones = len(list_pokemons)
    print(f'\n========HAY {cant_pokemones} POKEMON(ES) AGREGADO(S)=========\n')
    print('█ Nombre █ Fecha-Nacimiento █ Tipo-Sangre █ Signo-Zodiacal █ Tipos █\n')
    for n in list_pokemons:
        sig = sig_zod(n.dia_nacimiento, n.mes_nacimiento)
        print(f'█ {n.nombre_poke} █ {n.dia_nacimiento}/{n.mes_nacimiento}/{n.year_nacimiento} █ {n.tipo_sangre} █ {sig} █',', '.join(n.lista_type_pokemons),' █')
    print('\n================================================')

    pokemon_encontrado = False
    while True:
        export_YN = input(':█=¿Qué POKEMON deseas exportar? "e" para ir a menu=█: ')

        for z in list_pokemons:
            if export_YN == z.nombre_poke:
                pokemon_encontrado = True
                break
            elif export_YN == 'e':
                try:
                    os.system('cls')
                except:
                    os.system('clear')
                menu()
        if pokemon_encontrado:
            break
        else:
            print(':█==ERROR AL EXPORTAR POKEMON, INTENTELO==█: ')

    print('================================================\n')

    if os.path.isfile('datos.dat') and os.path.exists(f'Exportados/{export_YN}'):
        unir_tipos = ''

        for n in list_pokemons:
            edad = 2018-int(n.year_nacimiento)
            sig = sig_zod(n.dia_nacimiento, n.mes_nacimiento)
            if export_YN == n.nombre_poke:
                try:
                    patron_nums = 1
                    try:
                        os.mkdir(f'Exportados/{n.nombre_poke}')
                    except:
                        pass

                    dirs_exist = os.listdir(f'Exportados/{n.nombre_poke}/.')
                    pos_html_base = dirs_exist[-1]
                    lista_split = pos_html_base.split('-')
                    patron_nums = int(lista_split[-2]) + 1
                    unir_tipos = ', '.join(n.lista_type_pokemons)
                except:
                    pass

                with open(f'Exportados/{n.nombre_poke}/{n.nombre_poke}-{patron_nums}-.html', 'w') as create_html:
                    code_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="ISO-8859-1" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Pokemons</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" media="screen" href="css/style.css" />
        <link href="images/icon.png" rel="shortcut icon" type="image/x-icon">
    </head>
    <body>
        <div class="contenedor">
            <header class="header">
                <h1>DATOS DEL POKEMON</h1>
            </header>
            <section>
                <article>
                    <table>
                        <thead>
                            <tr>
                                <th colspan="3">{n.nombre_poke}</th>
                            </tr>
                        </thead>
                        <tr>
                            <td>Nombre del pokemon</td>
                            <td>{n.nombre_poke}</td>
                            <th rowspan="8" class="th-img-sprite"><img class="img-sprite" src="{n.sprites}"></th>
                        </tr>
                        <tr>
                            <td>Tipo(s)</td>
                            <td>{unir_tipos}</td>
                        </tr>
                        <tr>
                            <td>Tipo de Sangre</td>
                            <td>{n.tipo_sangre}</td>
                        </tr>
                        <tr>
                            <td>Comida Favorita</td>
                            <td>{n.comida_favorit}</td>
                        </tr>
                        <tr>
                            <td>Fecha de nacimiento</td>
                            <td>{n.dia_nacimiento}/{n.mes_nacimiento}/{n.year_nacimiento}</td>
                        </tr>
                        <tr>
                            <td>Signo zodiacal</td>
                            <td>{sig}</td>
                        </tr>
                        <tr>
                            <td>Edad</td>
                            <td>{edad}</td>
                        </tr>
                    </table>
                </article>
            </section>
            <footer>
                <p>Yander Sánchez &copy; Copyright 2018. Todos los Derechos Reservados.</p>
            </footer>
        </div>
    </body>
    </html>
                    """
                    create_html.write(code_html)
        try:
            os.system('cls')
        except:
            os.system('clear')
        print('================================================')
        print('============Exportado exitosamente==============')
        print('================================================')

    else:
        try:
            os.mkdir('Exportados')
            os.mkdir(f'Exportados/{export_YN}')
            os.mkdir(f'Exportados/{export_YN}/images')
            os.mkdir(f'Exportados/{export_YN}/css')
            shutil.copy(f'css/style.css', f'Exportados/{export_YN}/css/style.css')
            shutil.copy(f'images/background.jpg', f'Exportados/{export_YN}/images/background.jpg')
            shutil.copy(f'images/fondo-table.jpg', f'Exportados/{export_YN}/images/fondo-table.jpg')
        except:
            os.mkdir(f'Exportados/{export_YN}')
            os.mkdir(f'Exportados/{export_YN}/images')
            os.mkdir(f'Exportados/{export_YN}/css')
            shutil.copy(f'css/style.css', f'Exportados/{export_YN}/css/style.css')
            shutil.copy(f'images/background.jpg', f'Exportados/{export_YN}/images/background.jpg')
            shutil.copy(f'images/fondo-table.jpg', f'Exportados/{export_YN}/images/fondo-table.jpg')

        unir_tipos = ''

        for n in list_pokemons:
            edad = 2018 - int(n.year_nacimiento)
            sig = sig_zod(n.dia_nacimiento, n.mes_nacimiento)
            if export_YN == n.nombre_poke:
                patron_nums = 1
                try:
                    dirs_exist = os.listdir(f'Exportados/{n.nombre_poke}/.')
                    pos_html_base = dirs_exist[-1]
                    lista_split = pos_html_base.split('-')
                    patron_nums = int(lista_split[-2]) + 1
                except:
                    pass

                unir_tipos = ', '.join(n.lista_type_pokemons)

                with open(f'Exportados/{n.nombre_poke}/{n.nombre_poke}-{patron_nums}-.html', 'w') as create_html:
                    code_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="ISO-8859-1" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Pokemons</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" media="screen" href="css/style.css" />
        <link href="images/icon.png" rel="shortcut icon" type="image/x-icon">
    </head>
    <body>
        <div class="contenedor">
            <header class="header">
                <h1>DATOS DEL POKEMON</h1>
            </header>
            <section>
                <article>
                    <table>
                        <thead>
                            <tr>
                                <th colspan="3">{n.nombre_poke}</th>
                            </tr>
                        </thead>
                        <tr>
                            <td>Nombre del pokemon</td>
                            <td>{n.nombre_poke}</td>
                            <th rowspan="8" class="th-img-sprite"><img class="img-sprite" src="{n.sprites}"></th>
                        </tr>
                        <tr>
                            <td>Tipo(s)</td>
                            <td>{unir_tipos}</td>
                        </tr>
                        <tr>
                            <td>Tipo de Sangre</td>
                            <td>{n.tipo_sangre}</td>
                        </tr>
                        <tr>
                            <td>Comida Favorita</td>
                            <td>{n.comida_favorit}</td>
                        </tr>
                        <tr>
                            <td>Fecha de nacimiento</td>
                            <td>{n.dia_nacimiento}/{n.mes_nacimiento}/{n.year_nacimiento}</td>
                        </tr>
                        <tr>
                            <td>Signo zodiacal</td>
                            <td>{sig}</td>
                        </tr>
                        <tr>
                            <td>Edad</td>
                            <td>{edad}</td>
                        </tr>
                    </table>
                </article>
            </section>
            <footer>
                <p>Yander Sánchez &copy; Copyright 2018. Todos los Derechos Reservados.</p>
            </footer>
        </div>
    </body>
    </html>
                    """
                    create_html.write(code_html)
        try:
            os.system('cls')
        except:
            os.system('clear')
        print('================================================')
        print('============Exportado exitosamente==============')
        print('================================================')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def exportMapPokemons():

    html_base = plantilla_base()

    lista_final_code = []

    for n in list_pokemons:
        edad = 2018 - int(n.year_nacimiento)
        markers = f"""
        L.marker([{n.latitud},{n.longitud}])
				.addTo(map)
				.bindPopup('Nombre: {n.nombre_poke}, Edad: {edad}');
        """
        lista_final_code.append(markers)

    separar_markers ='\n'.join(lista_final_code)

    html_base = html_base.replace("{replace}", separar_markers)

    try:
        os.mkdir('html_base')
        shutil.copy('htmlbase.html', 'html_base/htmlbase.html')
        os.mkdir('Ubicaciones')
        with open('html_base/htmlbase.html', 'w') as write_marker_html:
            write_marker_html.write(html_base)

        shutil.move('html_base/htmlbase.html', 'Ubicaciones/htmlbase.html')

    except:
        if os.path.exists('Ubicaciones'):
            with open('html_base/htmlbase.html', 'w') as write_marker_html:
                write_marker_html.write(html_base)

            shutil.move('html_base/htmlbase.html', 'Ubicaciones/htmlbase.html')
    try:
        os.system('cls')
    except:
        os.system('clear')
    print('================================================')
    print('=====POKEMONES EXPORTADOS SATISFACTORIAMENTE====')
    input('==========ENTER PARA REGRESAR AL MENU===========')
    try:
        os.system('cls')
    except:
        os.system('clear')
    menu()

def sig_zod(dia_nacimiento, mes_nacimiento):
    dia_nacimiento = int(dia_nacimiento)
    mes_nacimiento = int(mes_nacimiento)
    SIGNO = ''

    if (mes_nacimiento==3 and dia_nacimiento>=21 and dia_nacimiento<=31) or (mes_nacimiento==4 and dia_nacimiento<=19 and dia_nacimiento>0):
        SIGNO = 'ARIES'
    elif (mes_nacimiento==4 and dia_nacimiento>=20 and dia_nacimiento<=30) or (mes_nacimiento==5 and dia_nacimiento<=20 and dia_nacimiento>0):
        SIGNO = 'TAURO'
    elif (mes_nacimiento==5 and dia_nacimiento>=21 and dia_nacimiento<=31) or (mes_nacimiento==6 and dia_nacimiento<=20 and dia_nacimiento>0):
        SIGNO = 'GÉMINIS'
    elif (mes_nacimiento==6 and dia_nacimiento>=21 and dia_nacimiento<=30) or (mes_nacimiento==7 and dia_nacimiento<=22 and dia_nacimiento>0):
        SIGNO = 'CÁNCER'
    elif (mes_nacimiento==7 and dia_nacimiento>=23 and dia_nacimiento<=31) or (mes_nacimiento==8 and dia_nacimiento<=22 and dia_nacimiento>0):
        SIGNO = 'LEO'
    elif (mes_nacimiento==8 and dia_nacimiento>=23 and dia_nacimiento<=31) or (mes_nacimiento==9 and dia_nacimiento<=22 and dia_nacimiento>0):
        SIGNO = 'VIRGO'
    elif (mes_nacimiento==9 and dia_nacimiento>=23 and dia_nacimiento<=30) or (mes_nacimiento==10 and dia_nacimiento<=22 and dia_nacimiento>0):
        SIGNO = 'LIBRA'
    elif (mes_nacimiento==10 and dia_nacimiento>=23 and dia_nacimiento<=31) or (mes_nacimiento==11 and dia_nacimiento<=21 and dia_nacimiento>0):
        SIGNO = 'ESCORPIÓN'
    elif (mes_nacimiento==11 and dia_nacimiento>=22 and dia_nacimiento<=30) or (mes_nacimiento==12 and dia_nacimiento<=20 and dia_nacimiento>0):
        SIGNO = 'SAGITARIO'
    elif (mes_nacimiento==12 and dia_nacimiento>=21 and dia_nacimiento<=31) or (mes_nacimiento==1 and dia_nacimiento<=20 and dia_nacimiento>0):
        SIGNO = 'CAPRICORNIO'
    elif (mes_nacimiento==1 and dia_nacimiento>=21 and dia_nacimiento<=31) or (mes_nacimiento==2 and dia_nacimiento<=19 and dia_nacimiento>0):
        SIGNO = 'ACUARIO'
    elif (mes_nacimiento==2 and dia_nacimiento>=20 and dia_nacimiento<=29) or (mes_nacimiento==3 and dia_nacimiento<=20 and dia_nacimiento>0):
        SIGNO = 'PISCIS'
    else:
        SIGNO = 'Signo-invalido'

    return SIGNO

def obtener_datos_pokemons(pokemon_link=''):
    datos_pokemons = {
        'name': '',
        'types': '',
        'sprites': 0,
    }

    solicitar = requests.get(pokemon_link)

    if solicitar.status_code == 404:
        return

    datos_json = solicitar.json()

    datos_pokemons['name'] = datos_json['name']
    datos_pokemons['types'] = datos_json['types']
    datos_pokemons['sprites'] = datos_json['sprites']['front_default']

    return datos_pokemons

def plantilla_base():
    with open('htmlbase.html', 'r') as export_map:
        contenido = export_map.read()
        return contenido

menu()