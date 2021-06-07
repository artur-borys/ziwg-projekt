import fasttext

def train_fasttext(filePath, type):
    print("Training fastText started...")
    global model
    model = fasttext.train_unsupervised(filePath, type)
    return model

