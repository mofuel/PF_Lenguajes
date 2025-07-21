# Importa la app desde el módulo principal
from app.main import create_app

# Crea una instancia de la app Flask
app = create_app()

# Ejecuta la app si este archivo es el principal
if __name__ == "__main__":
    app.run(debug=True)  # Inicia el servidor en modo debug
