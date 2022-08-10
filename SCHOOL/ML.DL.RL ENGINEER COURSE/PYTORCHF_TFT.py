from pytorch_forecasting import TemporalFusionTransformer


def TFT(training, learning_rate, hidden_size, attention_head_size, dropout, hidden_continuous_size, output_size, loss, reduce_on_plateau_patience):
    tft = TemporalFusionTransformer.from_dataset(
        training,
        # not meaningful for finding the learning rate but otherwise very important
        learning_rate=learning_rate,
        hidden_size=hidden_size,  # most important hyperparameter apart from learning rate
        # number of attention heads. Set to up to 4 for large datasets
        attention_head_size=attention_head_size,
        dropout=dropout,  # between 0.1 and 0.3 are good values
        hidden_continuous_size=hidden_continuous_size,  # set to <= hidden_size
        output_size=output_size,  # 7 quantiles by default
        loss=loss,
        # reduce learning rate if no improvement in validation loss after x epochs
        reduce_on_plateau_patience=reduce_on_plateau_patience,
    )
    return tft