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
                #inplace=True
            )
        ])
        return

    def predict(self, X, feature_names):
        X = self.img_transform(X.astype(np.uint8)).cuda()
        X = torch.stack([X] * 128, dim=0)
        #y_pred = self.model(X.unsqueeze(0))
        y_pred = self.model(X)
        softmax = torch.exp(y_pred - torch.max(y_pred, 0).values)
        softmax /= torch.sum(softmax)
        return softmax.cpu().detach().numpy()

