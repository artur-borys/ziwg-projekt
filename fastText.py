import fasttext

def train_fasttext(english=False):
    print("Training fastText started...")
    if english:
        return fasttext.load_model("fastTextModel-EN.bin")
    else:
        return fasttext.load_model("fastTextModel-PL.bin")

