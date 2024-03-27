from flask import Flask, request, render_template_string, send_file
import qrcode
import io
import base64

app = Flask(__name__)

# Ana sayfa
@app.route('/', methods=['GET', 'POST'])
def index():
    url = None
    qr_code = None
    alert_message = None

    if request.method == 'POST':
        url = request.form.get('url')

        if url:
            qr_code = generate_qr(url)
            alert_message = 'QR kod başarıyla oluşturuldu! Qr kodu cihaz ile kontrol ediniz. Oluştulan adres:  '+str(url)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title> QR Code Generator</title>
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            /* Additional custom styles */
            .my-alert {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">            
            <h2>QR Code Generator</h2>
            {% if alert_message %}
                <div class="alert alert-success my-alert" role="alert">
                    {{ alert_message }}
                </div>
            {% endif %}
            {% if qr_code %}
                <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code" class="img-fluid">
                <form method="GET" action="/download">
                    <input type="hidden" name="qr_code" value="{{ qr_code }}">
                    <button type="submit" class="btn btn-primary">QR Kodunu İndir</button>
                </form>
            {% endif %}
            <form method="POST">
                <div class="form-group">
                    <label for="urlInput">URL girin</label>
                    <input type="text" class="form-control" id="urlInput" name="url" placeholder="URL">
                </div>
                <button type="submit" class="btn btn-primary">QR Kodu Oluştur</button>
            </form>
        </div>
        <!-- Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    ''', url=url, qr_code=qr_code, alert_message=alert_message)

# QR kodunu oluşturmak için yardımcı işlev
def generate_qr(url):
    qr = qrcode.make(url, box_size=10)  # QR kodu sabit boyutta (10x10) oluşturulur

    # QR kodunu bir byte dizisine kaydet
    img_stream = io.BytesIO()
    qr.save(img_stream, 'PNG')
    img_stream.seek(0)
    img_bytes = img_stream.read()

    # Byte dizisini base64 formatına dönüştür
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    return img_base64

# QR kodunu indirmek için rota
@app.route('/download')
def download_qr():
    qr_code = request.args.get('qr_code')
    img_bytes = base64.b64decode(qr_code)

    return send_file(io.BytesIO(img_bytes), mimetype='image/png', as_attachment=True, download_name='qr_code.png')

if __name__ == '__main__':
    app.run(debug=True)
