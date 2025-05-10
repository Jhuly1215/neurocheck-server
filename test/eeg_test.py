import requests

# URL de tu endpoint FastAPI
url = "http://localhost:8000/api/predict-eeg"

# Ruta al archivo .set que quieres enviar
file_path = r"C:\Users\cesar\Desktop\projects\neurocheck-server\test\sub-018_task-eyesclosed_eeg.set"

# Montamos el multipart/form-data
with open(file_path, "rb") as f:
    files = {
        "file": (file_path, f, "application/octet-stream")
    }
    # Si tu endpoint espera algún campo adicional, lo añades en 'data={...}'
    response = requests.post(url, files=files)

# Imprimimos el código de estado HTTP y la respuesta JSON
print("Status code:", response.status_code)
print("Response JSON:", response.json())
