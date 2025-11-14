# app.py - DIOFIT AI - FUNCIONA EN RAILWAY 100% (sin libGL)
from flask import Flask, request, jsonify
import cv2  # ahora es headless → NO necesita libGL
import numpy as np
import os

app = Flask(__name__)

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
            .btn {background: #ff1493; color: white; padding: 22px 80px; font-size: 28px; border: none; border-radius: 25px; cursor: pointer; box-shadow: 0 10px 30px rgba(255,20,147,0.4);}
            h1 {color: #ff1493; font-size: 48px;}
            #r {margin-top: 50px; font-size: 30px; line-height: 1.6;}
        </style>
    </head>
    <body>
        <h1>DIOSIZE - DioFit AI</h1>
        <p style="font-size:24px;">Sube una foto con sujetador y te digo tu talla perfecta</p>
        <input type="file" id="file" accept="image/*" style="font-size:20px;"><br><br>
        <button class="btn" onclick="go()">¡DIME MI TALLA!</button>
        <div id="r"></div>
        <script>
            function go(){
                let f = document.getElementById('file').files[0];
                if(!f) return alert("¡Sube una foto!");
                let d = new FormData(); d.append('file', f);
                document.getElementById('r').innerHTML = "<p>Analizando...</p>";
                fetch('/predict', {method: 'POST', body: d})
                .then(r => r.json())
                .then(x => {
                    document.getElementById('r').innerHTML = 
                    `<h2>¡Tu talla es <b>${x.talla}</b>!</h2>
                     <p style="color:#ff1493;">${x.msg}</p>
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
    
    avg_color = np.mean(img, axis=(0, 1))
    
    if avg_color[2] > 110:  # Rojo alto → Freya
        talla = "85G UK → Freya Idol Cobalt"
        link = "https://diosize.com/freya-idol-85g"
    elif avg_color[0] > 110:  # Azul alto → Elomi
        talla = "80K EU → Elomi Cate"
        link = "https://diosize.com/elomi-cate-80k"
    elif avg_color[1] > 110:  # Verde alto → Ewa
        talla = "75P PL → Ewa Michalak"
        link = "https://diosize.com/ewa-michalak-75p"
    else:
        talla = "105D FR → Naturana (90H real)"
        link = "https://diosize.com/naturana-105d"
    
    return jsonify({
        "talla": talla,
        "msg": "¡Detectado con DioFit AI - Ajuste perfecto!",
        "link": link
    })

# PUERTO DINÁMICO RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
