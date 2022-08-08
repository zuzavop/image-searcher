import os
import clip
import torch
from PIL import Image

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)

path = "../photos"
text_path = "../nounlist.txt"

for fn in os.listdir(path):
    if (int(fn[:-4]) > 0):
        filename = path + "/" + fn
        image_input = preprocess(Image.open(filename)).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        text_features = torch.load('result.pt')
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(5)

        if not os.path.exists('result/' + fn[:-4] + '.txt'):
            os.mknod('result/' + fn[:-4] + '.txt')

        with open('result/' + fn[:-4] + '.txt', 'a') as f:
            for value, index in zip(values, indices):
                f.write(f"{index}: {100 * value.item():.2f},\n")


        print(str(fn[:-4]))
