import torch
import torch.nn as nn

class ResNetBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(channels, channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(channels), nn.ReLU(),
            nn.Conv1d(channels, channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(channels)
        )
    def forward(self, x): return torch.relu(self.net(x) + x)

class AuraDistinguisher(nn.Module):
    def __init__(self, channels=64, depth=5):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv1d(1, channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(channels), nn.ReLU(),
            nn.Conv1d(channels, channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(channels), nn.ReLU()
        )
        self.res_blocks = nn.Sequential(*[ResNetBlock(channels) for _ in range(depth)])
        self.fc = nn.Linear(channels, 1)

    def forward(self, x):
        x = self.stem(x.unsqueeze(1))
        x = self.res_blocks(x)
        x = x.mean(dim=2)
        return torch.sigmoid(self.fc(x))
