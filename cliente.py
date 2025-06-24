import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\n--- Cliente de Consola: Gestor de Tareas ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver sistema (/tareas)")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_bienvenida()
        elif opcion == "4":
            break
        else:
            print("Opción inválida")

def registrar():
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    response = requests.post(f"{BASE_URL}/registro", json=data)

    print(f"Status: {response.status_code}")
    print(response.json())

def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    response = requests.post(f"{BASE_URL}/login", json=data)

    print(f"Status: {response.status_code}")
    print(response.json())

def ver_bienvenida():
    response = requests.get(f"{BASE_URL}/tareas")
    if response.status_code == 200:
        print("HTML recibido:")
        print(response.text)
    else:
        print("Error al cargar la página:", response.status_code)

if __name__ == "__main__":
    menu()
