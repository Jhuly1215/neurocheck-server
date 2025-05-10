# app/routes/predict_eeg_routes.py
import os
import tempfile
import numpy as np
import torch
import torch.nn as nn
from fastapi import APIRouter, UploadFile, File, HTTPException
import mne

router = APIRouter()

# --- Parámetros (ajusta si hace falta) ---
SFREQ       = 500
WIN_SEC     = 2.0
WIN_SAMPLES = int(SFREQ * WIN_SEC)
DEVICE      = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH  = r"app\utils\eeg\best_shallow.pt"  # cámbialo a donde guardaste tu .pt


# --- Define aquí tu ShallowConvNet idéntico al que entrenaste ---
class ShallowConvNet(nn.Module):
    def __init__(self, n_chans, n_times, f1=20, dropout=0.3):
        super().__init__()
        self.conv1 = nn.Conv2d(1, f1, (1, 25), padding=(0,12))
        self.conv2 = nn.Conv2d(f1, f1, (n_chans,1), bias=False)
        self.pool  = nn.MaxPool2d((1,75), stride=(1,15))
        self.drop  = nn.Dropout(dropout)
        # computa dinámicamente el tamaño del flatten
        with torch.no_grad():
            x = torch.zeros(1,1,n_chans,n_times)
            x = torch.relu(self.conv1(x))
            x = torch.relu(self.conv2(x))
            x = self.pool(x)
            flat_dim = x.numel() // x.shape[0]
        self.fc = nn.Linear(flat_dim, 2)
    def forward(self, x):
        x = x.unsqueeze(1)                 # (B,1,CH,T)
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = self.pool(x)
        x = self.drop(x)
        return self.fc(x.flatten(1))


@router.post("/predict-eeg")
async def predict_eeg(file: UploadFile = File(...)):
    # 1) Validar extensión
    if not file.filename.lower().endswith(".set"):
        raise HTTPException(400, "Solo se aceptan archivos .set de EEGLAB")
    # 2) Guardar temporalmente
    contents = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".set", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # 3) Cargar con MNE
        raw = mne.io.read_raw_eeglab(tmp_path, preload=True, verbose=False)
    except Exception as e:
        raise HTTPException(400, f"No pude leer el .set: {e}")
    finally:
        os.unlink(tmp_path)

    # 4) Pre-procesamiento
    raw.resample(SFREQ, npad="auto", verbose=False)
    data = raw.get_data()  # shape (n_chans, n_times)
    n_chans, n_times = data.shape

    # 5) Segmentar en ventanas de WIN_SAMPLES
    n_win = n_times // WIN_SAMPLES
    if n_win < 1:
        raise HTTPException(400, f"El archivo dura menos de {WIN_SEC}s")
    segments = []
    for w in range(n_win):
        seg = data[:, w*WIN_SAMPLES:(w+1)*WIN_SAMPLES]
        # normalizar por canal
        seg = (seg - seg.mean(axis=1, keepdims=True)) / \
              (seg.std(axis=1, keepdims=True) + 1e-12)
        segments.append(seg.astype(np.float32))
    X = np.stack(segments)  # (n_win, n_chans, WIN_SAMPLES)

    # 6) Cargar modelo
    model = ShallowConvNet(n_chans, WIN_SAMPLES, f1=20, dropout=0.3).to(DEVICE)
    state = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(state)
    model.eval()

    # 7) Inferencia (probabilidad de "enfermo" = clase 1)
    probs = []
    with torch.no_grad():
        for seg in X:
            x = torch.from_numpy(seg).unsqueeze(0).to(DEVICE)  # (1,CH,T)
            logits = model(x)
            p = torch.softmax(logits, dim=1)[0,1].item()
            probs.append(p)
    avg_prob = float(np.mean(probs))
    pred = int(avg_prob >= 0.5)

    return {
        "prediction": pred,
        "probability": avg_prob,
        "window_probs": probs
    }
