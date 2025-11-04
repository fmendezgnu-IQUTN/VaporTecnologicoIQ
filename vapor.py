from pyXSteam.XSteam import XSteam
import os
import time
import sys
from pint import UnitRegistry

# --------------------------------------------------------------
# Sistemas de unidades

# steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS) # m/kg/sec/°C/bar/W
# steamTable = XSteam(XSteam.UNIT_SYSTEM_FLS) # ft/lb/sec/°F/psi/btu
# steamTable = XSteam(XSteam.UNIT_SYSTEM_BARE) # m/kg/sec/K/MPa/W

ureg = UnitRegistry()
ureg.formatter.default_format = '.3f'
Q_ = ureg.Quantity

# Conversión de Unidades y Equivalencias
# Potencias

CV = 1
btuh = 2546.1369922
kcalh = 641.61556828
KJh = 2684.5195377
lbph = 1980000
W = 745.69987158

# Colores para la consola
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BRILLANTE = "\033[1m"
OPACO = "\033[2m"
SUBRAYADO = "\033[4m"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def OPCION_INVALIDA(): # Función auxiliar del archivo original
    print(ROJO + "Opción inválida" + RESET)
    tiempo()

def tiempo():
    time.sleep(0.2)

global steam_table, tempu, presu, tiemu, longu, potu, masu

def MenuPrincipal():
    print(CYAN + f"======== APLICACIÓN DE UTILIDADES PARA TECNOLOGÍA DE LA ENERGÍA TÉRMICA ========\n" + RESET +\
    BRILLANTE + F"Elija opción:\n" \
    "1. Datos de Agua Saturada\n" \
    "2. Conversor de Unidades\n" \
    "0. Salir"+ RESET)

    op = int(input("Escriba opción: "))

    return op

def vaporagua(su):
    global steam_table, tempu, presu, tiemu, longu, potu, masu
    match su:
        case 1: 
            steam_table = XSteam(XSteam.UNIT_SYSTEM_MKS)
            longu = "m"
            tempu = "ºC"
            tiemu = "seg"
            presu = "bares"
            potu = "KJ"
            masu = "kg"
        case 2:
            steam_table = XSteam(XSteam.UNIT_SYSTEM_FLS)
            longu = "ft"
            tempu = "ºF"
            tiemu = "seg"
            presu = "psi"
            potu = "BTU"
            masu = "lb"
        case 3:
            steam_table = XSteam(XSteam.UNIT_SYSTEM_BARE)
            longu = "m"
            tempu = "K"
            tiemu = "seg"
            presu = "MPa"
            potu = "KJ"
            masu = "kg"
        case _:
            OPCION_INVALIDA()
            su = int(input(f"Por favor ingrese opción para sistema de unidades correcta: "))
            while su<1 or su>3:
                su = int(input(f"Por favor ingrese opción para sistema de unidades correcta: "))
    
    return steam_table

def saturacion(steam_table):
    pot = str(input("Temperatura o Presión de Saturación? T o P: ")).lower()
    while pot!="t" and pot !="p":
        pot = input("Valor incorrecto, ingrese temperatura o presión de Saturación? T o P: ").lower()
    match pot:
        case "t":
            tsat = float(input("Ingrese temperatura de saturación: "))
            psat = steam_table.psat_t(tsat)               
            h_vapor = steam_table.hV_t(tsat)
            h_liq = steam_table.hL_t(tsat)
            cpv = steam_table.CpV_t(tsat)
            cpl = steam_table.CpL_t(tsat)
        case "p":
            psat = input("Ingrese presión de saturación: ")
            num = psat.replace(",",".")
            try:
                psat = float(num)
            except ValueError:
                print("El valor ingresado no es un número.")
            tsat = steam_table.tsat_p(psat)
            h_vapor = steam_table.hV_p(psat)
            h_liq = steam_table.hL_p(psat)
            cpv = steam_table.CpV_p(psat)
            cpl = steam_table.CpL_p(psat)
        case _:
            print("Opción Inválida")

    landa = h_vapor - h_liq

    return pot, tsat, psat, h_liq, h_vapor, cpl, cpv, landa

def realizar_conversion(unidades_dict, categoria):
    """
    Función genérica para pedir datos al usuario y realizar una conversión con Pint.
    """
    # 1. Mostrar las unidades disponibles
    print(BRILLANTE + f"Unidades disponibles:"+ RESET)
    for key, value_tuple in unidades_dict.items():
        print(BRILLANTE +f"{key}. {value_tuple[0]}"+ RESET)
    
    print(AMARILLO + "0. Volver al menú de categorías" + RESET)
    # 2. Pedir datos al usuario
    unidad_origen_key = input("Elija la unidad de ORIGEN (o 0 para Volver): ")
    if unidad_origen_key == "0":
        return
    valor_str = input("Ingrese la cantidad a convertir: ")
    unidad_destino_key = input("Elija la unidad de DESTINO: ")

    try:
        # 3. Convertir el valor a número y obtener las unidades del diccionario
        valor_origen = float(valor_str)
        unidad_origen_str = unidades_dict[unidad_origen_key][1] 
        unidad_destino_str = unidades_dict[unidad_destino_key][1] 

        # 4. Crear la cantidad con Pint
        if categoria == "temperatura":
            # Para Temp (C, F, R, K) usamos Q_() para crear una cantidad absoluta
            cantidad_origen = Q_(valor_origen, ureg(unidad_origen_str))
        else:
            # Para Potencia (y otras) usamos la multiplicación (son deltas)
            cantidad_origen = valor_origen * ureg(unidad_origen_str)

        # 5. Realizar la conversión (¡la magia de Pint!)
        cantidad_destino = cantidad_origen.to(unidad_destino_str)

        # 6. Mostrar el resultado
        print("-" * 30)
        origen_display = unidades_dict[unidad_origen_key][0]
        destino_display = unidades_dict[unidad_destino_key][0]
        
        print(BRILLANTE + f"Resultado: {valor_origen:.2f} {origen_display} son {cantidad_destino.magnitude:.2f} {destino_display}" + RESET)
        print("-" * 30)

    except KeyError:
        print("Error: Opción de unidad no válida. Por favor, elija un número de la lista.")
    except ValueError:
        print("Error: La cantidad a convertir debe ser un número.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def resultados(tsat, psat, h_vapor, h_liq, landa, cpv, cpl):
    print(BRILLANTE+f"="*15 + "RESULTADOS" + "="*15 +RESET)
    print(CYAN + f"1. Temperatura de Saturación: " + RESET + BRILLANTE + f"{tsat:.1f} {tempu}"+ RESET)
    print(CYAN + f"2. Presión de Saturación: "+ RESET + BRILLANTE + f"{psat:.2f} {presu}" + RESET)
    print(CYAN + f"3. Entalpia de vapor saturado H: "+ RESET + BRILLANTE + f"{h_vapor:.2f} {potu}/{masu}"+ RESET)
    print(CYAN + f"4. Entalpía de líquido saturado h: "+ RESET + BRILLANTE + f"{h_liq:.2f} {potu}/{masu}"+ RESET)
    print(CYAN + f"5. Calor latente λ: "+ RESET + BRILLANTE + f"{landa:.1f} {potu}/{masu}"+ RESET)
    print(CYAN + f"6. Calor Específico del Vapor Cpv: "+ RESET + BRILLANTE + f"{cpv:.2f} {potu}/{masu} {tempu}"+ RESET)
    print(CYAN + f"7. Calor Específico del Líquido Cpl: "+ RESET + BRILLANTE + f"{cpl:.2f} {potu}/{masu} {tempu}"+ RESET)
    print(BRILLANTE + f"================================================="+ RESET)

# --------------------------------------------------------------------------------------------------------------------------------------------------
# Definición de Unidades:

unidades_potencia = {
    "1": ("HP (Caballos de fuerza)", "hp"),
    "2": ("BTU por hora", "BTU/hour"),
    "3": ("Kilocalorías por hora", "kcal/hour"),
    "4": ("Kilojoules por hora", "kJ/hour"),
    "5": ("Watt", "watt")
}

unidades_temperatura = {
    "1": ("Celsius", "degC"),
    "2": ("Fahrenheit", "degF"),
    "3": ("Kelvin", "kelvin"),
    "4": ("Rankine", "degR")
}

unidades_presion = {
    "1": ("Pascal", "Pa"),
    "2": ("Kilopascal","kPa"),
    "3": ("Bar","bar"),
    "4": ("Atmósfera","atm"),
    "5": ("PSI (lb/pulg2)","psi"),
    "6": ("mmHg","mmHg"),
    "7": ("kg-fuerza/cm2","kgf / cm**2")
}
unidades_energia = {
    "1": ("Joule","joule"),
    "2": ("kilojoule", "kJ"),
    "3": ("Caloria","cal"),
    "4": ("kilocaloria","kcal"),
    "5": ("BTU","BTU"),
    "6": ("W/h","watt_hour"),
    "7": ("KW/h", "kWh")
}

u_cp = {
    "1": ("J/kg.K","J / (kg * K)"),
    "2": ("KJ/kg.°C","kJ / (kg * delta_degC)"),
    "3": ("BTU/lb.°F","BTU / (lb * delta_degF)")
}

u_condtermica = {
    "1": ("W/m.K","W / (m * K)"),
    "2": ("BTU/h.pie.°F", "BTU / (hr * ft * delta_degF)")
}

u_coeftcalor = {
    "1": ("BTU/h.pie2.°F", "BTU / (hr * ft**2 * delta_degF)"),
    "2": ("W/h.m2.K", "W / (m**2 * K)")
}

u_caudalvol = {
    "1": ("m3/seg", "m**3/s"),
    "2": ("m3/h", "m**3/hr"),
    "3": ("L/seg", "L / s"),
    "4": ("L/min", "L / min"),
    "5": ("pie3/min", "ft**3 / min"),
    "6": ("pie3/seg", "ft**3 / s")
}

un_caudalmas = {
    "1": ("kg/seg", "kg / s"),
    "2": ("kg/h", "kg / hr"),
    "3": ("lb/h", "lb / hr"),
    "4": ("Ton/h", "tonne / hr")
}

un_densidad = {
    "1": ("kg/m3", "kg / m**3"),
    "2": ("g/cm3", "g / cm**3"),
    "3": ("lb/pie3", "lb / ft**3")
}

un_viscosidad = {
    "1": ("Pa.seg", "Pa * s"),
    "2": ("Poise", "poise"),
    "3": ("Centipoise", "cP"),
    "4": ("lb/pie.seg", "lb / (ft * s)")
}

un_long = {
    "1": ("metro", "m"),
    "2": ("centimetro", "cm"),
    "3": ("milimetro","mm"),
    "4": ("pulgada", "inch"),
    "5": ("pie", "ft")
}

un_area = {
    "1": ("Metro Cuadrado", "m**2"),
    "2": ("Centimetro Cuadrado", "cm**2"),
    "3": ("Pie Cuadrado", "ft**2"),
    "4": ("Pulgada Cuadrada","inch**2")
}

un_volumen ={
    "1": ("Metro Cúbico", "m**3"),
    "2": ("Litro", "L"),
    "3": ("Mililitro", "mL"),
    "4": ("Pie Cúbico", "ft**3")
}
# --------------------------------------------------------------

pc = True
while pc:
    op = MenuPrincipal()

    if op ==0:
        print(BRILLANTE + f"Gracias por usar la versión de prueba - Tecnología de la Energía Térmica - UTN FRRo"+ RESET)
        time.sleep(1)
        pc = False

    menu = True
    while menu:
        match op:
            case 1:
                limpiar_pantalla()
                vaph20 = True
                while vaph20:
                    print(CYAN + f"========== Datos de vapor de agua - TET UTN FRRo: =========="+ RESET)
                    print("Hay que elegir el sistema de unidades con el que trabajar")
                    print(BRILLANTE + f"1. SI: m/kg/sec/°C/bar/W \n" 
                    "2. Sistema imperial: ft/lb/sec/°F/psi/btu\n" 
                    "3. SI con kelvin y pascales: m/kg/sec/K/MPa/W \n"
                    "0. Volver al menú \n "+ RESET)

                    su = int(input(f"Ingrese opción para sistema de unidades: "))

                    match su:
                        case 1:
                            st = vaporagua(su)

                            pot, tsat, psat, h_liq, h_vapor, cpl, cpv, landa = saturacion(st)
                            print("\n")
                            resultados(tsat, psat, h_vapor, h_liq, landa, cpv, cpl)
                            input("Presione una tecla para continuar")
                            limpiar_pantalla()
                        case 2:
                            st = vaporagua(su)

                            pot, tsat, psat, h_liq, h_vapor, cpl, cpv, landa = saturacion(st)
                            print("\n")
                            resultados(tsat, psat, h_vapor, h_liq, landa, cpv, cpl)
                            input("Presione una tecla para continuar")
                            limpiar_pantalla()
                        case 3:
                            st = vaporagua(su)

                            pot, tsat, psat, h_liq, h_vapor, cpl, cpv, landa = saturacion(st)
                            print("\n")
                            resultados(tsat, psat, h_vapor, h_liq, landa, cpv, cpl)
                            input("Presione una tecla para continuar")
                            limpiar_pantalla()
                        case 0:
                            limpiar_pantalla()
                            vaph20 = False
                        case _:
                            OPCION_INVALIDA()
                menu = False
                limpiar_pantalla()
            case 2:
                limpiar_pantalla()
                conver = True
                while conver:
                    limpiar_pantalla()
                    print(CYAN + f"========== Conversión de Unidades - TET UTN FRRo: =========="+ RESET)
                    print("Elegir categoria")
                    print(BRILLANTE + f"1. Potencia \n" \
                        "2. Temperatura\n"
                        "3. Presión\n"
                        "4. Energía\n"
                        "5. Calor Específico\n"
                        "6. Conductividad Térmica K\n"
                        "7. Coeficiente de Transmisión de Calor U\n"
                        "8. Fluidos y Caudales\n"
                        "9. Básicas\n"
                        "0. Volver"+ RESET)  

                    op = int(input("Opción: "))

                    match op:
                        case 1:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Potencia ---"+ RESET)
                            realizar_conversion(unidades_potencia, "potencia")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 2:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Temperatura ---"+ RESET)
                            realizar_conversion(unidades_temperatura, "temperatura")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 3:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Presión ---"+ RESET)
                            realizar_conversion(unidades_presion, "presion")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 4:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Energía ---"+ RESET)
                            realizar_conversion(unidades_energia, "energia")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 5:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Calor Específico ---"+ RESET)
                            realizar_conversion(u_cp, "caloresp")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 6:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Conductividad Térmica K ---"+ RESET)
                            realizar_conversion(u_condtermica, "condtermicaK")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()
                        case 7:
                            limpiar_pantalla()
                            print(CYAN + f"\n--- Conversión de Coeficiente de Transmisión de Calor U ---"+ RESET)
                            realizar_conversion(u_coeftcalor, "coeftcalorU")
                            input("Presione una tecla para volver al menu")
                            limpiar_pantalla()           
                        case 8:
                            fyc = True
                            while fyc:
                                limpiar_pantalla()
                                print(CYAN + f"========== Conversión de Unidades de Fluidos y Caudales - TET UTN FRRo: =========="+ RESET)
                                print("Elegir categoria")
                                print(BRILLANTE + f"1. Caudal Volumétrico \n" \
                                "2. Caudal Másico\n" \
                                "3. Densidad\n" \
                                "4. Viscosidad\n" \
                                "0. Volver\n" + RESET)  

                                opfc = int(input("Opción: "))

                                match opfc:
                                    case 1:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Caudal Volumétrico ---"+ RESET)
                                        realizar_conversion(u_caudalvol, "caudalvol")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 2:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Caudal Másico ---"+ RESET)
                                        realizar_conversion(un_caudalmas, "caudalmas")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla()    
                                    case 3:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Densidad ---"+ RESET)
                                        realizar_conversion(un_densidad, "densidad")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 4:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Viscosidad ---"+ RESET)
                                        realizar_conversion(un_viscosidad, "viscosidad")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 0:
                                        limpiar_pantalla()
                                        fyc = False
                                    case _:
                                        OPCION_INVALIDA()
                        case 9:
                            ubas = True
                            while ubas:
                                limpiar_pantalla()
                                print(CYAN + f"========== Conversión de Unidades Básicas - TET UTN FRRo: =========="+ RESET)
                                print("Elegir categoria")
                                print(BRILLANTE + f"1. Longitud \n" \
                                "2. Área\n" \
                                "3. Volumen\n" \
                                "0. Volver\n" + RESET)  

                                opub = int(input("Opción: "))

                                match opub:
                                    case 1:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Longitudes ---"+ RESET)
                                        realizar_conversion(un_long, "longitud")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 2:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Áreas ---"+ RESET)
                                        realizar_conversion(un_area, "areas")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 3:
                                        limpiar_pantalla()
                                        print(CYAN + f"\n--- Conversión de Volúmenes ---"+ RESET)
                                        realizar_conversion(un_volumen, "volumen")
                                        input("Presione una tecla para volver al menu")
                                        limpiar_pantalla() 
                                    case 0:
                                        limpiar_pantalla()
                                        ubas = False
                                    case _:
                                        OPCION_INVALIDA()
                        case 0:
                            limpiar_pantalla()
                            conver = False
                        case _:
                            OPCION_INVALIDA()
            case 0:
                menu = False
            case _:
                OPCION_INVALIDA()








