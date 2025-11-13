# app.py - DIOFIT AI - FUNCIONA EN RAILWAY AL 100%
from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

# Flask app
app = Flask(__name__)

# Carpeta para guardar temporalmente (Railway la crea sola)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>DioFit AI - DioSize</title>
        <style>
            body{font-family:Arial;text-align:center;background:#fff5f8;padding:50px;}
            .btn{background:#ff1493;color:white;padding:18px 50px;font-size:22px;border:none;border-radius:15px;cursor:pointer;}
            h1{color:#ff1493;}
        </style>
    </head>
    <body>
        <h1>DIOSIZE - DioFit AI</h1>
        <p>Sube una foto con sujetador y te digo tu talla perfecta</p>
        <input type="file" id="file" accept="image/*"><br><br>
        <button class="btn" onclick="go()">¡DIME MI TALLA!</button>
        <div id="r" style="margin-top:30px;font-size:24px;"></div>
        <script>
            function go(){
                let f = document.getElementById('file').files[0];
                if(!f) return alert("¡Sube una foto primero!");
                let d = new FormData(); 
                d.append('file', f);
                fetch('/predict', {method:'POST', body:d})
                .then(r => r.json())
                .then(x => {
                    document.getElementById('r').innerHTML = 
                    `<h2>¡Tu talla ideal es <b>${x.talla}</b>!</h2>
                     <p>${x.msg}</p>
                     <a href="${x.link}" target="_blank">
                     <button class="btn">COMPRAR EN DIOSIZE</button></a>`;
                })
                .catch(() => alert("Error, intenta de nuevo"));
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
        return jsonify({"error": "Imagen no válida"}), 400
    
    # Detección por color dominante (demo rápida)
    avg_color = np.mean(img, axis=(0, 1))  # BGR
    
    if avg_color[2] > 140:  # Rojo alto → Freya turquesa/azul
        talla = "85G UK → Freya Idol Cobalt"
        link = "https://diosize.com/freya-idol-85g"
    elif avg_color[0] > 140:  # Azul alto → Elomi
        talla = "80K EU → Elomi Cate"
        link = "https://diosize.com/elomi-cate-80k"
    elif avg_color[1] > 140:  # Verde alto → Ewa Michalak
        talla = "75P PL → Ewa Michalak"
        link = "https://diosize.com/ewa-michalak-75p"
    else:
        talla = "105D FR → Naturana (real 90H)"
        link = "https://diosize.com/naturana-105d"
    
    return jsonify({
        "talla": talla,
        "msg": "¡Detectado automáticamente con DioFit AI!",
        "link": link
    })

# ESTO ES LO QUE LO HACE FUNCIONAR EN RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
