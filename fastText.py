import fasttext

def train_fasttext():
    print("Training fastText started...")
    model = fasttext.load_model("fastTextModel.bin")
    return model

