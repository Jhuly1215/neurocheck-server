# app/utils/eeg/model_loader.py
import os
import torch
import torch.nn as nn

# Asegúrate de usar exactamente la misma definición de arquitectura
class ShallowConvNet(nn.Module):
    def __init__(self, n_chans, n_times, f1=20, dropout=0.3):
        super().__init__()
        self.conv1 = nn.Conv2d(1, f1, (1, 25), padding=(0,12))
        self.conv2 = nn.Conv2d(f1, f1, (n_chans,1), bias=False)
        self.pool  = nn.MaxPool2d((1,75), stride=(1,15))
        self.drop  = nn.Dropout(dropout)
        # calcular dinámicamente el tamaño flattened
        with torch.no_grad():
            x = torch.zeros(1,1,n_chans,n_times)
            x = torch.relu(self.conv1(x))
            x = torch.relu(self.conv2(x))
            x = self.pool(x)
            flat_dim = x.numel() // x.shape[0]
        self.fc = nn.Linear(flat_dim, 2)
    def forward(self, x):
        x = x.unsqueeze(1)
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = self.pool(x)
        x = self.drop(x)
        return self.fc(x.flatten(1))

_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_eeg_model():
    global _model
    if _model is None:
        # Ajusta esta ruta a donde guardaste best_shallow.pt
        weights_path = os.path.join(os.getcwd(), "best_shallow.pt")
        # Debes saber cuántos canales y muestras espera el modelo:
        # Por ejemplo, si tu dataset tiene 60 canales y ventanas de 1000 muestras:
        n_chans = 60
        n_times =  int(500 * 2.0)  # sfreq * win_sec
        mdl = ShallowConvNet(n_chans, n_times, f1=20, dropout=0.3)
        mdl.load_state_dict(torch.load(weights_path, map_location=_device))
        mdl.to(_device).eval()
        _model = mdl
    return _model
