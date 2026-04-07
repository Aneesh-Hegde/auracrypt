import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from speck import Speck32
from model import AuraDistinguisher
from utils import generate_dataset, _pair_to_bits
from solver import recover_key_with_z3
import time

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

ROUNDS, EPOCHS, SAMPLES, BATCH_SIZE = 3, 15, 400000, 1024

def train_and_heist():
    x_train, y_train = generate_dataset(SAMPLES, ROUNDS)
    loader = DataLoader(TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)), batch_size=BATCH_SIZE, shuffle=True)
    
    model = AuraDistinguisher().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.004, steps_per_epoch=len(loader), epochs=EPOCHS)
    criterion = nn.BCELoss()

    for epoch in range(EPOCHS):
        model.train()
        for bx, by in loader:
            bx, by = bx.to(device).float(), by.to(device).float().view(-1, 1)
            optimizer.zero_grad()
            out = model(bx); loss = criterion(out, by); loss.backward()
            optimizer.step(); scheduler.step()
        print(f"Epoch {epoch+1:2d} Completed.")

    # Narrative Demo
    key_real = 0x1122334455667788
    cipher = Speck32(key=key_real)
    p_test = [(0x1337, 0xBEEF), (0xCAFE, 0xBABE)]
    intercepted = [(pt, cipher.encrypt(pt, ROUNDS)) for pt in p_test]

    print("\n--- AURACRYPT FORENSIC REPORT ---")
    model.eval()
    with torch.no_grad():
        c0, c1 = intercepted[0][1], cipher.encrypt((p_test[0][0]^0x0040, p_test[0][1]), ROUNDS)
        bits = torch.from_numpy(_pair_to_bits(c0, c1)).float().unsqueeze(0).to(device)
        conf = model(bits).item()
    
    print(f"AI Signal Confidence: {conf*100:.2f}%")
    rec, elap = recover_key_with_z3(intercepted, ROUNDS)
    print(f"Recovered Key: {rec} in {elap:.4f}s")
    print(f"Master Match: {int(rec,16) == key_real}")

if __name__ == "__main__":
    train_and_heist()
