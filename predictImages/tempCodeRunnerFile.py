from keras.models import load_model

# Load the trained model
model = load_model("D:/Workspace/Visual Studio Code/4th_Year/2st_Term/XLA/WebPredict/predictImages/models/best_cnn_seg_model.h5", compile=False)