# BIGAI SCHOOL SMALL PROJECTS
# LD_TOOL
Language Detector Tool

*⭐️ INSTALL REQUIREMENTS:*
pip install -r requirements.txt

*⭐️ RECREATE CONDA ENVIROMENT:*
conda env create -f LD_TOOL.yml

### MAIN MODULES WITH EXPLANATION:
* data - directory contain files from Tatoeba + dummy Unify_data.py script for unification data.Result is data_lang.csv
* data_arch.py - data architecture file.Use data_lang.csv to create datasets and dataloaders for training.Also language for numerical values
* model_arch - mapping hidden states from BERT to number of classes(here 4 - 4 languages).Dropuout for regularization.Attention mask for padding tokens
* LD_TOOL_TRAIN - Save, Load model methods for save after each epoch and load for later use.It use LanguageModelDataset(data_arch) and LanguageClassifier(model_arch).It sets optimizer and loss(CrossEntropy for a classification problem).Its evaluate model after each epoch.
* LD_TOOL_PERF - Load saved model and get predictions using val_data_loader.Later we visualize this predictions as Confiusion matrix, classification distributions and prediction distributions 

### EXPLANATION AS VIDEO ON YT:
https://youtu.be/YMDSjfe51BM

Enjoy!

Aleksander Majos