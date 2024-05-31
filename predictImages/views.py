from django.shortcuts import render
from django.http import JsonResponse
from keras.models import load_model
from .predict import load_image, predict_and_plot

model = load_model("D:/Workspace/Visual Studio Code/4th_Year/2st_Term/XLA/Pneumonia_Prediction/predictImages/models/best_cnn_seg_model.h5", compile=False)

def index(request):
    return render(request, "predict.html")

def predict_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]
        img = load_image(image_file)
        label, image_base64 = predict_and_plot(model, img)
        image_url = f"data:image/png;base64,{image_base64}"

        return JsonResponse({"label": label, "image_url": image_url})

    return JsonResponse({"error": "No image provided"}, status=400)
