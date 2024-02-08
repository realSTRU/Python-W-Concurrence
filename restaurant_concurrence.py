import threading
import time

# Definimos los recursos disponibles en el restaurante
recursos = {
    'cubiertos': 3,
    'cucharas': 4,
    'cucharitas_postre': 3,
    'cuchillos': 4
}

# Creamos un semáforo para controlar el acceso concurrente a los recursos
semaphore = threading.Semaphore()

# Función para verificar si hay suficientes utensilios disponibles
def verificar_recursos_suficientes(orden):
    for recurso, cantidad in orden.items():
        if recursos[recurso] < cantidad:
            return False
    return True

# Definimos la función para atender a una persona
def atender_persona(persona, orden):
    try:
        # Utilizamos el semáforo para garantizar la exclusión mutua al acceder a los recursos
        with semaphore:
            # Mostramos los recursos disponibles antes de atender a la persona
            print("\nRecursos disponibles antes de atender a", persona)
            for recurso, cantidad in recursos.items():
                print(f"{recurso}: {cantidad}")
            
            # Verificamos si hay suficientes recursos para atender la orden
            while not verificar_recursos_suficientes(orden):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"No hay suficientes utensilios para atender a {persona}. Esperando...")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                time.sleep(1)  # Esperamos 1 segundo y volvemos a verificar
            
            # Si hay suficientes recursos, actualizamos los recursos disponibles
            for recurso, cantidad in orden.items():
                recursos[recurso] -= cantidad

            # Mostramos por pantalla que se está atendiendo a la persona con su orden y utensilios utilizados
            print(f"\n¡Saludos chicos!\nAhora se está atendiendo a {persona} con {', '.join([f'{cantidad} {recurso}' for recurso, cantidad in orden.items()])}")
            
            # Simulamos el tiempo de preparación
            time.sleep(2)
            
            # Mostramos los recursos disponibles después de atender a la persona
            print("\nRecursos disponibles después de atender a", persona)
            for recurso, cantidad in recursos.items():
                print(f"{recurso}: {cantidad}")
            print("--------------------------------------------")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Liberamos los recursos utilizados después de 3 segundos
        time.sleep(5)
        for recurso, cantidad in orden.items():
                recursos[recurso] += cantidad
        # Liberamos los recursos utilizados
        semaphore.release()
        # Imprimimos que la persona ha sido liberada
        
        print(f"\nLa persona {persona} ha sido liberada. Se devuelven los siguientes recursos: {', '.join([f'{cantidad} {recurso}' for recurso, cantidad in orden.items()])}")
       
# Definimos las órdenes de las personas
ordenes = [
    {'Persona 1': {'cubiertos': 1, 'cucharas': 1, 'cucharitas_postre': 1}},
    {'Persona 2': {'cubiertos': 1, 'cuchillos': 1, 'cucharitas_postre': 1}},
    {'Persona 3': {'cubiertos': 1, 'cuchillos': 1, 'cucharitas_postre': 1}},
    {'Persona 4': {'cubiertos': 1, 'cucharas': 1, 'cuchillos': 1, 'cucharitas_postre': 1}},
    {'Persona 5': {'cubiertos': 1, 'cuchillos': 1}}
]

# Creamos y ejecutamos los hilos para atender a cada persona con su orden
hilos = []
for orden in ordenes:
    for persona, orden_persona in orden.items():
        hilo = threading.Thread(target=atender_persona, args=(persona, orden_persona))
        hilo.start()
        hilos.append(hilo)

# Esperamos a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

# Mostramos los recursos disponibles al final
print("\nRecursos disponibles finales:")
for recurso, cantidad in recursos.items():
    print(f"{recurso}: {cantidad}")
