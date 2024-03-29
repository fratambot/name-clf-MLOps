# import json
import numpy as np
import os
import sys
import tensorflow as tf
import tensorflow.keras.layers as tfl

# import wandb

# we use /app folder as base_path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# and we add it at the beginning of PYTHONPATH otherwise we
# cannot import from modules at the same level
sys.path.insert(0, base_path)

# config_filepath = os.path.join(base_path, "config.json")
# global CONFIG
# CONFIG = json.load(open(config_filepath))


def CNN_LSTM_model(input_shape=16, embedding_size=33, softmax_units=7, dense_1=32):
    print("Hello model")
    # wandb.login()
    # with wandb.init(project=PROJECT_NAME, job_type="initialize", config=default_config) as run: # noqa: E501
    #     wb_config = wandb.config
    #     print(wb_config)

    embedding_weigths = np.concatenate(
        (
            [np.zeros((embedding_size), dtype=int)],
            np.identity(embedding_size, dtype="int"),
        ),
        axis=0,
    )

    # Build Sequential model
    model = tf.keras.Sequential()
    model.add(tfl.Input(shape=(input_shape,), name="input_layer", dtype="int64"))
    model.add(
        tfl.Embedding(
            embedding_size + 1,
            embedding_size,
            input_length=input_shape,
            weights=[embedding_weigths],
        )
    )
    model.add(
        tfl.Conv1D(
            filters=16, kernel_size=7, strides=1, activation="relu", padding="valid"
        )
    )
    # model.add(
    #     tfl.Conv1D(
    #         filters=16, kernel_size=5, strides=1, activation="relu", padding="valid"
    #     )
    # )
    # model.add(
    #     tfl.Conv1D(
    #         filters=16, kernel_size=3, strides=1, activation="relu", padding="valid"
    #     )
    # )
    model.add(tfl.MaxPooling1D(pool_size=2))
    model.add(tfl.Dropout(rate=0.3))
    model.add(tfl.LSTM(input_shape, return_sequences=True))
    # model.add(tfl.Dropout(rate=0.4))
    # model.add(
    #     tfl.LSTM(8,return_sequences=True)
    # )
    model.add(tfl.Flatten())
    model.add(
        tfl.Dense(
            name="dense_1",
            units=dense_1,
            activation="relu",
        )
    )
    model.add(
        tfl.Dense(
            name="dense_2",
            units=128,
            activation="relu",
        )
    )
    # Softmax
    model.add(tfl.Dense(name="softmax", units=softmax_units, activation="softmax"))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
        loss="categorical_crossentropy",
        metrics=[tf.keras.metrics.CategoricalAccuracy()],
    )

    print(model.summary())

    return model
