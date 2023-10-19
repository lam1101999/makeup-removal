from train.GAN.models import Generator
from torchvision import transforms
import torch
import os
import pathlib
import numpy as np


class MakeupRemover():
    def __init__(self):
        state_dict_path = os.path.join(pathlib.Path(__file__), "model_weight", "model30")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        generator_state_dict = torch.load(state_dict_path, map_location=torch.device(device))
        self.generator = Generator()
        self.generator.load_state_dict(generator_state_dict["G_XtoY"])
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])


    def remove_makeup(self, image):
        image = self.transform(image)
        image = image[None,:]
        remove_makeup_image = self.generator(image)
        remove_makeup_image = self.deprocess(remove_makeup_image)
        remove_makeup_image = remove_makeup_image[0]
        return remove_makeup_image
    def denormalize(self,images, std=0.5, mean=0.5):
        # For plot
        images = (images * std) + mean
        return images


    def deprocess(self,input_tensor):
        return np.transpose(self.denormalize(input_tensor.detach().cpu().numpy()), (0, 2, 3, 1))