import torch
import torch.nn as nn
from transformers import  AdamW, get_linear_schedule_with_warmup
import os
from data_arch import LanguageDataset, LanguageModelDataset
from model_arch import LanguageClassifier


def save_model(model, optimizer, scheduler, epoch, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'scheduler_state_dict': scheduler.state_dict(),
    }, path)

def load_model(path, model, optimizer=None, scheduler=None):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    if optimizer:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    if scheduler:
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    epoch = checkpoint['epoch']
    return model, optimizer, scheduler, epoch


def train_epoch(
        model,
        data_loader,
        loss_fn,
        optimizer,
        device,
        scheduler,
        n_examples
):
    model = model.train()
    losses = 0
    correct_predictions = 0

    for d in data_loader:
        input_ids = d['input_ids'].to(device)
        attention_mask = d['attention_mask'].to(device)
        labels = d['labels'].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        loss = loss_fn(outputs, labels)

        _, preds = torch.max(outputs, dim=1)
        correct_predictions += torch.sum(preds == labels)
        losses += loss.item()

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    return correct_predictions.double() / n_examples, losses / n_examples

def eval_model(model, data_loader, loss_fn, device, n_examples):
    model = model.eval()
    losses = 0
    correct_predictions = 0

    with torch.no_grad():
        for d in data_loader:
            input_ids = d['input_ids'].to(device)
            attention_mask = d['attention_mask'].to(device)
            labels = d['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            loss = loss_fn(outputs, labels)

            _, preds = torch.max(outputs, dim=1)
            correct_predictions += torch.sum(preds == labels)
            losses += loss.item()

    return correct_predictions.double() / n_examples, losses / n_examples


def main():
    lmd = LanguageModelDataset()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LanguageClassifier(n_classes=lmd.N_CLASSES)
    model = model.to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
    total_steps = len(lmd.train_data_loader) * lmd.EPOCHS

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )

    loss_fn = nn.CrossEntropyLoss().to(device)

    for epoch in range(lmd.EPOCHS):
        print(f'Epoch {epoch + 1}/{lmd.EPOCHS}')
        print('-' * 10)

        train_acc, train_loss = train_epoch(
            model,
            lmd.train_data_loader,
            loss_fn,
            optimizer,
            device,
            scheduler,
            len(lmd.train_dataset)
        )

        print(f'Train loss {train_loss} accuracy {train_acc}')

        val_acc, val_loss = eval_model(
            model,
            lmd.val_data_loader,
            loss_fn,
            device,
            len(lmd.val_dataset)
        )

        print(f'Val   loss {val_loss} accuracy {val_acc}')

        save_model(model, optimizer, scheduler, epoch, f'./model/language_model_epoch_{epoch}.bin')


if __name__ == "__main__":
    main()
