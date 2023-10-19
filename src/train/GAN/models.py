import torch

class ConvBlock(torch.nn.Module):
    def __init__(self, output_channels, kernel_size, stride=1, padding=0, activation=torch.nn.ReLU) -> None:
        super().__init__()
        self.block = torch.nn.Sequential(
            torch.nn.LazyConv2d(output_channels, kernel_size=kernel_size, stride=stride,
                                padding=padding),
            torch.nn.BatchNorm2d(output_channels),
            torch.nn.ReLU(),
        )

    def forward(self, x) -> torch.Tensor:
        return self.block(x)


class DeConvBlock(torch.nn.Module):
    def __init__(self, output_channels, kernel_size, stride=1, padding=0,
                 output_padding=0, activation=torch.nn.ReLU) -> None:
        super().__init__()
        self.block = torch.nn.Sequential(
            torch.nn.LazyConvTranspose2d(output_channels, kernel_size=kernel_size,
                                         stride=stride, padding=padding, output_padding=output_padding),
            torch.nn.BatchNorm2d(output_channels),
            activation()
        )

    def forward(self, x) -> torch.Tensor:
        return self.block(x)


class ResidualBlock(torch.nn.Module):
    def __init__(self, output_channels, kernel_size, stride=1, padding=0, activation=torch.nn.ReLU):
        super().__init__()
        self.block = torch.nn.Sequential(
            torch.nn.LazyConv2d(output_channels, kernel_size, stride, padding),
            torch.nn.ReflectionPad2d(1),
            torch.nn.BatchNorm2d(output_channels),
            activation(),
            torch.nn.LazyConv2d(output_channels, kernel_size, stride, padding),
            torch.nn.ReflectionPad2d(1),
            torch.nn.BatchNorm2d(output_channels)
        )

    def forward(self, input_tensor) -> torch.Tensor:
        x = self.block(input_tensor)
        x = x + input_tensor
        return x


def replace_layers(model):
    for n, module in model.named_children():
        if len(list(module.children())) > 0:
            # compound module, go inside it
            replace_layers(module)
        if isinstance(module, torch.nn.MaxPool2d):
            setattr(model, n, torch.nn.Conv2d)


class Generator(torch.nn.Module):
    def __init__(self, input_channels=3, output_channels=3, filters=64, n_blocks=9) -> None:
        super().__init__()
        down_scale = [torch.nn.ReflectionPad2d(3),
                      ConvBlock(output_channels=filters, kernel_size=7,
                                activation=torch.nn.LeakyReLU),
                      ConvBlock(output_channels=filters*2, kernel_size=3,
                                stride=2, padding=1, activation=torch.nn.LeakyReLU),
                      ConvBlock(output_channels=filters*4, kernel_size=3, stride=2, padding=1, activation=torch.nn.LeakyReLU)]
        for i in range(n_blocks):
            down_scale.append(ResidualBlock(
                output_channels=filters*4, kernel_size=3, activation=torch.nn.LeakyReLU))

        up_scale = [
            DeConvBlock(output_channels=filters*2, kernel_size=3, stride=2,
                        padding=1, output_padding=1, activation=torch.nn.LeakyReLU),
            DeConvBlock(output_channels=filters, kernel_size=3, stride=2,
                        padding=1, output_padding=1, activation=torch.nn.LeakyReLU),
            torch.nn.ReflectionPad2d(3),
            torch.nn.LazyConv2d(out_channels=output_channels,
                                kernel_size=7, stride=1, padding=0),
            torch.nn.Tanh()
        ]

        self.down_scale = torch.nn.Sequential(*down_scale)
        self.up_scale = torch.nn.Sequential(*up_scale)

    def forward(self, x) -> torch.Tensor:
        latent_vector = self.down_scale(x)
        fake_image = self.up_scale(latent_vector)
        return fake_image


class Discriminator(torch.nn.Module):
    def __init__(self, input_channels=3, filters=64) -> None:
        super().__init__()
        layers = [
            torch.nn.LazyConv2d(out_channels=filters,
                                kernel_size=4, stride=2, padding=1),
            torch.nn.LeakyReLU(),
            ConvBlock(output_channels=filters*2, kernel_size=4,
                      stride=2, padding=1, activation=torch.nn.LeakyReLU),
            ConvBlock(output_channels=filters*4, kernel_size=4,
                      stride=2, padding=1, activation=torch.nn.LeakyReLU),
            ConvBlock(output_channels=filters*8, kernel_size=4,
                      stride=1, padding=1, activation=torch.nn.LeakyReLU),
        ]
        # Output layers
        layers.append(torch.nn.LazyConv2d(out_channels=1,
                      kernel_size=4, stride=1, padding=1))
        self.model = torch.nn.Sequential(*layers)

    def forward(self, x) -> torch.Tensor:
        return self.model(x)
    
def weights_init(m):
    classname = m.__class__.__name__
    if hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
        torch.nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        torch.nn.init.normal_(m.weight.data, 1.0, 0.02)
        torch.nn.init.constant_(m.bias.data, 0)