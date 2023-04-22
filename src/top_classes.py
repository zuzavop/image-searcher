import os

import clip
import torch

# load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)

def classify_images(vectors_path, nounlist_path, result_file, top_k = 10):
    # load nounlist (text dataset) features
    text_features = torch.load(nounlist_path)

    for fn in os.listdir(vectors_path):
        filename = vectors_path + "/" + fn
        # load image features get from clip
        image_features = torch.load(filename)

        # get top 10 classes for image
        similarity = (100.0 * image_features @ text_features.T)
        values, indices = similarity[0].topk(top_k)

        with open(result_file, 'a') as f:
            f.write(fn[:-4] + ';' + str(list(indices)) + '\n')


