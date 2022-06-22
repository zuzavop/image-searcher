import torch
import clip
from PIL import Image
import numpy as np
import os


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

path = "photos"
for fn in os.listdir(path):
    filename = path + "/" + fn
    image = preprocess(Image.open(filename)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_feat = model.encode_image(image)
        torch.save(image_feat, f"clip/{fn[:-4]}.pt")


#clip = [] 
#for fn in sorted(os.listdir("clip")):
    #clip.append(torch.load(f"clip/{fn}"))
