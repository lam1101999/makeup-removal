# Makeup-removal
Try: [Click here](https://anti-makeup.streamlit.app/)

## Introduction
This is the project for my AI class, main objective is creating 2 models that can:
 - Classification if an image have makeup or no
 - Remove makeup of face in image

## How to run this project
Step 1: Clone project from github  
Step 2: Install python  
Step 3: Install library  
```pip install  -r requirements.txt```  
Step 4: Run project
```streamlit run src/main.py```

## How to train model
At first you need a dataset with format:
```
your_data_set
|--with: folder of makeup image
|
|--without: folder of non-makeup image
```
Then copy it to src/train/dataset

### Classification model
In src/train/classification/Classification.ipynb
Change the link to your dataset and run all cell

#### Remove makeup model
In src/train/GAN/GAN.ipynb
Change the link to your dataset and run all cell