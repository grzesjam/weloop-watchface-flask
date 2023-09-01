import os
import uuid
from flask import Flask, request, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

app.config['disable_file_manipulation'] = False
# Define the path to the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Define the allowed file extensions
app.config['ALLOWED_EXTENSIONS'] = {'png', 'bin'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if f.startswith('watchface_')]
    # get only filename of pngs
    files = [f.rsplit('.', 1)[0] for f in files if f.endswith('.png')]
    return render_template('index.html', files=files)


@app.route('/upload/', methods=['POST'])
def upload_file():
    if app.config['disable_file_manipulation']:
        return "File manipulation is disabled"
    random_uuid = uuid.uuid4()
    filepng = request.files['filepng']
    filebin = request.files['filebin']
    if filepng.content_type != 'image/png' or filebin.content_type != 'application/octet-stream':
        return "Invalid file type"

    filename = 'watchface_{}'.format(random_uuid)
    filepng.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.png"))
    filebin.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_bin.bin"))
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['get'])
def delete_file(filename):
    if app.config['disable_file_manipulation']:
        return "File manipulation is disabled"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(f"{file_path}.png"):
        os.remove(f"{file_path}.png")
        os.remove(f"{file_path}_bin.bin")

    return redirect(url_for('index'))


@app.route('/watch', methods=['get'])
def watch():
    domain = f"{request.scheme}://{request.host}"
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if f.startswith('watchface_')]
    # get only filename of pngs
    files = [f.rsplit('.', 1)[0] for f in files if f.endswith('.png')]
    answer = dict()
    answer["result"] = "0000"
    answer["message"] = "ok"
    answer["recordCount"] = len(files)
    answer["dataList"] = list()
    for i, value in enumerate(files):
        answer["dataList"].append({
            "watchNo": f"{i + 1:04d}",
            "watchClass": "00",
            "watchfaceImageURL": f"{domain}/uploads/{value}.png",
            "watchfaceBinURL": f"{domain}/uploads/{value}_bin.bin",
            "watchfaceUploadFileURL": f"{domain}/uploads/{value}.png",
            "name": f"{value}"
        })

    return answer

# Mock login responses for chronos eco
@app.route('/login.do', methods=['get', 'post'])
def loginMock():
    response = ('{"result":"0000","accessToken":"sampleAccessToken","age":"28","allRank":"1","averagepoint":"99",'
                '"birthday":"1995-05-10","compliancedays":"365","distance":"10",'
                '"headPic":"https://sample.com/image.jpg","nickname":"John Doe","openid":"sampleOpenid",'
                '"pointChampion":"66","pointCount":"550","runChampion":"25","sex":"M","sleepTime":"8",'
                '"stature":"175","useddate":"2023-02-01","userid":"sampleUserid","weekRank":"5","weight":"70"}')
    return response

@app.route('/get_personal_info.do', methods=['get', 'post'])
def getPersonalInfoMock():
    response = ('{"age":"28","allchampion":"1","averagepoint":"99","birthday":"1995-05-10","compliancedays":"365",'
                '"distances":"10","email":"johndoe@example.com","friendMark":"Y",'
                '"headPicUrl":"https://sample.com/image.jpg","nickname":"John Doe","pointChampion":"66",'
                '"poitCount":"550","runChampion":"25","sex":"M","stature":"175","useddate":"2023-02-01",'
                '"weekporintPercentage":"50","weekrunPercentage":"50","weight":"70"}')
    return response

if __name__ == '__main__':
    app.run(debug=True)
