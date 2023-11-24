import torchvision
import torch
import os
import pathlib
from torchvision import transforms
class Classifier():
    def __init__(self):
        self.weight_folder = os.path.join(pathlib.Path(
            __file__).parent, "model_weight")
        self.transform = transforms.Compose([
            transforms.Resize((96, 96)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
    def choose_model(self, model_name="resnet34"):
        """
        Selects and loads a pre-trained model based on the given `model_name`.

        Parameters:
            model_name (str): The name of the model to choose. Default is "resnet34".

        Returns:
            None
        """
        weight_path = os.path.join(self.weight_folder, f"{model_name}.pth")
        model_state_dict = torch.load(
            weight_path, map_location=torch.device(self.device)) 
        if model_name == "resnet34":
            self.model = torchvision.models.resnet34(num_classes=2)
            self.model.load_state_dict(model_state_dict)
            
        else:
            self.model = getattr(torchvision.models, model_name)(num_classes=2)
            self.model.load_state_dict(model_state_dict)
        
    def predict(self, image):
        """
        Predicts the output for a given image.

        Parameters:
            image (Tensor): The input image to be predicted.

        Returns:
            output (Tensor): The predicted output of the model.
        """
        
        if self.model is None:
            raise Exception("Please choose a model first")
        image = self.transform(image)
        image = image[None, :]
        self.model.eval()
        with torch.no_grad():
            output = self.model(image)
            output = torch.nn.functional.softmax(output, dim=1)
            predict_class = torch.argmax(output, dim=1)
            proba = output[:,predict_class].squeeze()
        return predict_class, proba
    
if __name__ == "__main__":
    # Test this class
    classifier = Classifier()
    classifier.choose_model("efficientnet_v2_l")
    print(classifier.model)