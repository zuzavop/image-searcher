# not used - problems with classification of images with damage

import os

import clip
import torch
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


def classify(photos_path, text_path, output_file, accuracy=0.8):
    idx2label = []
    with open(text_path) as f:
        for line in f:
            idx2label.append(line[:-1])

    text = clip.tokenize(idx2label).to(device)

    for photo in os.listdir(photos_path):
        filename = photos_path + "/" + photo
        image = preprocess(Image.open(filename)).unsqueeze(0).to(device)

        with torch.no_grad():
            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            result = [i for i in range(len(probs[0])) if probs[0][i] > accuracy]

        with open(output_file, 'a') as f:
            f.write(photo[:-4] + ':' + str(result) + ',/n')


