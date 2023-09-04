
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import smtplib
from flask import Flask , request, render_template
#from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

app = Flask(__name__)

model = load_model("dent_class.h5",compile=False)
                 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath,'uploads',f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)
        
        img = image.load_img(filepath,target_size = (64,64)) 
        x = image.img_to_array(img)
        print(x)
        x = np.expand_dims(x,axis =0)
        print(x)
        y=model.predict(x)
        preds=np.argmax(y, axis=1)
        #preds = model.predict_classes(x)
        print("prediction",preds)
        index = ['crack','dent','missing-head','paint-off','scratch']
        text =  str(index[preds[0]])
    return render_template('index.html', text=text,Success="Succesfull")


@app.route('/form',methods=['POST'])
def inde():
    return render_template('form.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    input_value = request.form.get('input_value')
    message=request.form.get('value1')
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('b210436@skit.ac.in','99426738')
    print(input_value)
    server.sendmail('b210436@skit.ac.in',input_value,message)
    print('mail sent')  
    return render_template('form.html',Status="Mail Send Successfully") 

@app.route('/back',methods=['POST'])
def back():
    return render_template('index.html')       
if __name__ == '__main__':
    app.run(debug = False, threaded = False)
