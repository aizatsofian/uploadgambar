import os
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Konfigurasi asas
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'kunci-rahsia-anda' # Perlu untuk flash message

# Fungsi untuk memeriksa jika sambungan fail dibenarkan
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Cipta direktori 'uploads' jika belum wujud
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # Memaparkan fail index.html dari folder 'templates'
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'gambar' not in request.files:
        flash('Tiada bahagian fail dikesan')
        return redirect(request.url)
    
    file = request.files['gambar']
    
    if file.filename == '':
        flash('Tiada fail dipilih')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        # secure_filename() untuk keselamatan nama fail
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Mesej kejayaan
        flash(f'Gambar "{filename}" berjaya dimuat naik!')
        return redirect(url_for('index'))
    else:
        flash('Jenis fail tidak dibenarkan. Sila muat naik fail imej (png, jpg, jpeg, gif).')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)