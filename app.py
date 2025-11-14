# app.py - DIOFIT AI v2 - DETECCIÓN REAL DE TALLA POR FOTO (YOLOv8)
from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = Flask(__name__)

# CARGA EL MODELO REAL (entrenado en 500 fotos)
MODEL_PATH = "best.pt"  # ← Sube este archivo a tu repo
model = YOLO(MODEL_PATH)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>DioFit AI - DioSize</title>
        <style>
            body {font-family: Arial; text-align: center; background: #fff5f8; padding: 60px;}
            .btn {background: #ff1493; color: white; padding: 25px 90px; font-size: 30px; border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 12px 40px rgba(255,20,147,0.4);}
            h1 {color: #ff1493; font-size: 52px;}
            #r {margin-top: 60px; font-size: 32px; line-height: 1.7;}
        </style>
    </head>
    <body>
        <h1>DIOSIZE - DioFit AI</h1>
        <p style="font-size:26px;">Sube una foto con sujetador puesto → te digo tu talla real</p>
        <input type="file" id="file" accept="image/*" style="font-size:22px;"><br><br>
        <button class="btn" onclick="go()">¡ANALIZA MI TALLA!</button>
        <div id="r"></div>
        <script>
            function go(){
                let f = document.getElementById('file').files[0];
                if(!f) return alert("¡Sube una foto!");
                let d = new FormData(); d.append('file', f);
                document.getElementById('r').innerHTML = "<p>IA analizando tu sujetador...</p>";
                fetch('/predict', {method: 'POST', body: d})
                .then(r => r.json())
                .then(x => {
                    document.getElementById('r').innerHTML = 
                    `<h2>¡Tu talla real es <b>${x.talla}</b>!</h2>
                     <p style="color:#ff1493;"><b>${x.msg}</b></p>
                     <a href="${x.link}" target="_blank">
                     <button class="btn">COMPRAR EN DIOSIZE.COM</button></a>`;
                })
                .catch(() => document.getElementById('r').innerHTML = "<p style='color:red;'>Error, intenta de nuevo</p>");
            }
        </script>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    filestream = file.read()
    img_array = np.frombuffer(filestream, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({"error": "Imagen inválida"}), 400

    # IA REAL: YOLOv8 detecta quad-boob, gore, banda, etc.
    results = model(img, conf=0.4)[0]
    
    # Mapeo de detecciones a tallas reales
    labels = [results.names[int(cls)] for cls in results.boxes.cls]
    
    if "quad-bo
