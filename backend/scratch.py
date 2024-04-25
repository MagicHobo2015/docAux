from tensorflow.keras.utils import image_dataset_from_directory


def main():
    train_ds = image_dataset_from_directory(
            dir,
            labels='inferred',
            seed=42,
            label_mode='categorical'
            )

    print(train_ds)

if __name__ == "__main__":
    main()