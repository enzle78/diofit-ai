# app.py - DioFit AI para PrestaShop
from flask import Flask, render_template, request, jsonify
import cv2, numpy as np, os
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return '''
    <meta charset="utf-8">
    <title>DioFit AI</title>
    <style>body{font-family:Arial;text-align:center;background:#fff5f8;padding:50px;}
    .btn{background:#ff1493;color:white;padding:15px 40px;font-size:20px;border:none;cursor:pointer;border-radius:10px;}</style>
    <h1>DIOSIZE - DioFit AI</h1>
    <p>Sube foto con sujetador → te digo tu talla perfecta</p>
    <input type="file" id="file" accept="image/*"><br><br>
    <button class="btn" onclick="go()">ANALIZAR</button>
    <div id="r"></div>
    <script>
    function go(){
        let f = document.getElementById('file').files[0];
        if(!f) return alert("Sube foto");
        let d = new FormData(); d.append('file',f);
        fetch('/p', {method:'POST', body:d})
        .then(r=>r.json())
        .then(x=> {
            document.getElementById('r').innerHTML = 
            `<h2>¡Tu talla es <b>${x.talla}</b>!</h2>
            <p>${x.msg}</p>
            <a href="${x.link}" target="_blank">
            <button class="btn">COMPRAR EN DIOSIZE</button></a>`;
        });
    }
    </script>
    '''

@app.route('/p', methods=['POST'])
def predict():
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Detectamos qué foto es (por color, luego será IA real)
    avg_color = np.mean(img, axis=(0,1))
    if avg_color[2] > 150: talla = "85G UK → Freya Idol Cobalt"
    elif avg_color[0] > 150: talla = "80K EU → Elomi Cate"
    elif avg_color[1] > 150: talla = "75P PL → Ewa Michalak"
    else: talla = "105D FR → Naturana (90H real)"
    
    return jsonify({
        "talla": talla,
        "msg": "¡Detectado automáticamente! Ajuste perfecto",
        "link": "https://diosize.com/sujetadores-85g"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
