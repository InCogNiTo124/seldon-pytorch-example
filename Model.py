import numpy as np
import torch
import pickle
from torchvision.transforms import Compose, Grayscale, Normalize, Resize, ToPILImage, ToTensor

class Model():
    def __init__(self, uri="", model_name="model.pkl"):
        with open(uri+model_name, 'rb') as f:
            self.model = pickle.load(f).float().eval().cuda()
        self.img_transform = Compose([
            ToPILImage(),
            Resize((224, 224)),
            Grayscale(3),
            ToTensor(),
            Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            )
        ])
        return

    def predict(self, X, feature_names):
        X = self.img_transform(X.astype(np.uint8)).cuda()
        X = torch.stack([X] * 2, dim=0)
        y_pred = self.model(X)
        y_max = torch.max(y_pred, 1, keepdim=True).values
        y_pred -= y_max
        softmax = torch.exp(y_pred - y_max)
        softmax /= torch.sum(softmax, 1, keepdim=True)
        return softmax.cpu().detach().numpy()

