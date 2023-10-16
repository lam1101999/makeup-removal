from collections import deque, namedtuple
import glob
import torch
from torch.utils.data import Dataset
import os
from PIL import Image

class GeneratorDataset(Dataset):
    """Load images from folder for generator."""

    def __init__(self, list_root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.list_root_dir = list_root_dir
        self.filenames = []
        for root_dir in list_root_dir:
            self.filenames.extend(glob.glob(root_dir + f'{os.sep}*.jpg'))
        self.transform = transform

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, iD_X):
        if torch.is_tensor(iD_X):
            iD_X = iD_X.tolist()

        img_path = self.filenames[iD_X]
        sample = Image.open(img_path).convert("RGB")
        if self.transform:
            sample = self.transform(sample)

        return sample


class ImageBuffer:
    """Fixed-size buffer to store image tuples."""

    def __init__(self, buffer_size):
        """Initialize a ImageBuffer object.
        Params
        ======
            buffer_size (int): maximum size of buffer
        """
        self.memory = deque(maxlen=buffer_size)  # internal memory (deque)
        self.images = namedtuple("Images", field_names=['real_image_X', 'fake_image_X',
                                                        'real_image_Y', 'fake_image_Y'])

    def add(self, real_image_X, fake_image_X, real_image_Y, fake_image_Y):
        """Add a new images to memory."""
        image_pair = self.images(
            real_image_X, fake_image_X.clone(), real_image_Y, fake_image_Y.clone())
        self.memory.append(image_pair)

    def sample(self):
        """Return a batch of image tuples from memory."""
        return self.memory.popleft()

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)

# custom weights initialization called on netG and netD


