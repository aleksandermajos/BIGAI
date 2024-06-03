from LD_TOOL_TRAIN import load_model
from model_arch import LanguageClassifier
from data_arch import LanguageModelDataset
import torch
from transformers import AdamW, get_linear_schedule_with_warmup
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd


def plot_confusion_matrix(cm, class_names):
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()

def plot_classification_report(y_true, y_pred, class_names):
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    df = pd.DataFrame(report).transpose()
    plt.figure(figsize=(10, 7))
    sns.heatmap(df.iloc[:-1, :].T, annot=True, cmap='Blues')
    plt.title('Classification Report')
    plt.show()

def plot_prediction_distribution(prediction_probs, class_names):
    prediction_probs = torch.nn.functional.softmax(prediction_probs, dim=1).numpy()
    plt.figure(figsize=(10, 7))
    for i, class_name in enumerate(class_names):
        sns.kdeplot(prediction_probs[:, i], label=class_name)
    plt.xlabel('Prediction probability')
    plt.ylabel('Density')
    plt.title('Prediction Probability Distribution')
    plt.legend()
    plt.show()

def get_predictions(model, data_loader, device):
    model = model.eval()
    texts = []
    predictions = []
    prediction_probs = []
    real_values = []

    with torch.no_grad():
        for d in data_loader:
            texts.extend(d['text'])
            input_ids = d['input_ids'].to(device)
            attention_mask = d['attention_mask'].to(device)
            labels = d['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            _, preds = torch.max(outputs, dim=1)
            texts.extend(d['text'])
            predictions.extend(preds)
            prediction_probs.extend(outputs)
            real_values.extend(labels)

    predictions = torch.stack(predictions).cpu()
    prediction_probs = torch.stack(prediction_probs).cpu()
    real_values = torch.stack(real_values).cpu()
    return texts, predictions, prediction_probs, real_values


def inference():
    lmd = LanguageModelDataset()
    model_path = f'./model/language_model_epoch_5.bin'

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LanguageClassifier(n_classes=lmd.N_CLASSES)
    model = model.to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps= len(lmd.train_data_loader) * lmd.EPOCHS
    )

    model, optimizer, scheduler, epoch = load_model(model_path, model, optimizer, scheduler)

    texts, predictions, prediction_probs, real_values = get_predictions(
        model,
        lmd.val_data_loader,
        device
    )

    y_pred = predictions.numpy()
    y_true = real_values.numpy()
    class_names = [lmd.id_to_language[i] for i in range(lmd.N_CLASSES)]

    # Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, class_names)

    # Plot classification report
    plot_classification_report(y_true, y_pred, class_names)

    # Plot prediction distribution
    plot_prediction_distribution(prediction_probs, class_names)




if __name__ == "__main__":
    inference()
