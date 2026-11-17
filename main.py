import random
import re
import os
import csv
import json
from datetime import datetime
from pymongo import MongoClient


registros_biomedicos = []


def registrar_log(mensaje):
    try:
        with open("log.txt", "a", encoding="utf-8") as archivo_log:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo_log.write(f"[{fecha_hora}] {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en el log: {e}")

def crear_estructura_carpetas():
    rutas = [os.path.join("data", "txt"), os.path.join("data", "csv"), os.path.join("data", "json")]
    for ruta in rutas:
        try:
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                registrar_log(f"Se creó el directorio: {ruta}")
        except Exception as e:
            registrar_log(f"Error al crear {ruta}: {e}")


def exportar_archivos():
    if not registros_biomedicos:
        print("Primero debes generar los datos (Opción 1).")
        return

    print("\n Exportando archivos a las carpetas...")
    try:
        ruta_txt = os.path.join("data", "txt", "pacientes.txt")
        with open(ruta_txt, "w", encoding="utf-8") as f:
            for p in registros_biomedicos:
                f.write(f"{p['id']}, {p['fr']}, {p['fc']}, {p['spo2']}\n")
        print("Archivo TXT guardado.")
        
        ruta_csv = os.path.join("data", "csv", "pacientes.csv")
        with open(ruta_csv, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "fr", "fc", "spo2"])
            writer.writeheader()
            writer.writerows(registros_biomedicos)
        print("Archivo CSV guardado.")
        
        ruta_json = os.path.join("data", "json", "pacientes.json")
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(registros_biomedicos, f, indent=4)
        print("Archivo JSON guardado.")
        
        registrar_log("Se exportaron exitosamente los formatos TXT, CSV y JSON.")
    except Exception as e:
        print(f"Error exportando archivos locales: {e}")
        registrar_log(f"Error archivos: {e}")


def validar_registro(id_val, fr_val, fc_val, spo2_val):
    patron_id = r"^ID-\d{3}$"
    patron_fr = r"^\d{2} Años$"
    patron_fc = r"^\d{3}ppm$"
    patron_spo2 = r"^\d{2,3}%$"
    
    if not re.match(patron_id, id_val): return False
    if not re.match(patron_fr, fr_val): return False
    if not re.match(patron_fc, fc_val): return False
    if not re.match(patron_spo2, spo2_val): return False
    return True

def generar_datos_aleatorios():
    registros_biomedicos.clear()
    print("\n Generando 50 registros biomédicos...")
    for i in range(1, 51):
        id_gen = f"ID-{i:03d}"
        fr_gen = f"{random.randint(18, 90):02d} Años"
        fc_gen = f"{random.randint(50, 150):03d}ppm"
        spo2_gen = f"{random.randint(80, 100)}%"
        
        if validar_registro(id_gen, fr_gen, fc_gen, spo2_gen):
            registros_biomedicos.append({"id": id_gen, "fr": fr_gen, "fc": fc_gen, "spo2": spo2_gen})
            
    registros_biomedicos.sort(key=lambda x: x['fc'])
    registrar_log("Se generaron y ordenaron 50 registros exitosamente.")
    print(f"Se generaron y ordenaron {len(registros_biomedicos)} registros.")


def operar_mongodb():
    if not registros_biomedicos:
        print("Primero debes generar los datos (Opción 1).")
        return

    print("\n Conectando a MongoDB Atlas...")
    usuario = 'miguelsantamariar_db_user' 
    clave = 'ThfhIxVqSXqPOXeB'
    stringConexion = f'mongodb+srv://{usuario}:{clave}@cluster0.1hphjei.mongodb.net/'
    
    try:
        cnx = MongoClient(stringConexion)
        db = cnx.taller3 
        coleccion = db.signos_vitales
        
        
        coleccion.delete_many({})
        
        
        coleccion.insert_many(registros_biomedicos)
        print("50 pacientes insertados en MongoDB Atlas (Colección: signos_vitales).")
        
     
        print("Procesando consultas matemáticas...")
        suma_fc = 0
        pacientes_riesgo_spo2 = []
        
        for doc in coleccion.find():
            doc.pop('_id', None) 
            
            
            fc_num = int(doc['fc'].replace('ppm', ''))
            spo2_num = int(doc['spo2'].replace('%', ''))
            
            suma_fc += fc_num
            
            if spo2_num < 94:
                pacientes_riesgo_spo2.append(doc)
                
        promedio_fc = suma_fc / 50
        print(f"Promedio de Frecuencia Cardiaca: {promedio_fc:.1f} ppm")
        print(f"Pacientes con SpO2 menor a 94%: {len(pacientes_riesgo_spo2)}")
        
      
        resultados = {
            "promedio_fc": f"{promedio_fc:.1f} ppm",
            "total_pacientes_riesgo_spo2": len(pacientes_riesgo_spo2),
            "pacientes_riesgo_detalles": pacientes_riesgo_spo2
        }
        
        ruta_mongo_json = os.path.join("data", "json", "resultados_mongo.json")
        with open(ruta_mongo_json, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=4)
            
        print(f"Archivo 'resultados_mongo.json' guardado en {ruta_mongo_json}")
        registrar_log("Interacción exitosa con MongoDB y exportación de consultas completada.")
        
    except Exception as e:
        print(f"Error con MongoDB: {e}")
        registrar_log(f"Error Mongo: {e}")


def menu():
    crear_estructura_carpetas()
    registrar_log("Inició el sistema.")
    
    while True:
        print("\n=== SISTEMA DE GESTIÓN BIOMÉDICA ===")
        print("1. Ingresar/Generar y Validar datos")
        print("2. Exportar datos locales (TXT, CSV, JSON)")
        print("3. Conectar a MongoDB y ejecutar consultas (Genera resultados_mongo.json)")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            generar_datos_aleatorios()
        elif opcion == '2':
            exportar_archivos()
        elif opcion == '3':
            operar_mongodb()
        elif opcion == '4':
            registrar_log("Se cerró el programa.")
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()