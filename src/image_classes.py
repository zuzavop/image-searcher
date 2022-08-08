import torch
import clip
from PIL import Image
import numpy as np
import os


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

path = "..\\..\\data\\photos"
text_path = "..\\nounlist.txt"
accuracy = 0.8

idx2label = []
with open(text_path) as f:
    for line in f:
        idx2label.append(line[:-1])

text = clip.tokenize(idx2label).to(device)

for fn in os.listdir(path):
    filename = path + "/" + fn
    image = preprocess(Image.open(filename)).unsqueeze(0).to(device)
    
    with torch.no_grad():    
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        result = [i for i in range(len(probs[0])) if probs[0][i] > accuracy]
        
	with open('result.csv', 'a') as f:
		f.write(fn[:-4] + ':' + str(result) + ',/n')

