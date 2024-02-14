import os

def pipeline():
        print("RNN_LSTM")
        os.system("python main.py -n RNN_LSTM")
        print("TextCNN")
        os.system("python main.py -n TextCNN")
        print("MLP")
        os.system("python main.py -n MLP")

if __name__ == "__main__":
        pipeline()
