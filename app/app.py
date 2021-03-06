from flask import Flask, request, redirect, url_for
from flask import render_template
from werkzeug import secure_filename
app = Flask(__name__)
import os
import io
import dill as pickle
import numpy as np
import pandas as pd
import chardet
import sys
import matplotlib.pyplot as plt
from movier import Movier


a = Movier() # used to clean the input srt file

def check_text(line):
    '''
    check if each line of srt file is text
    '''
    line = line.strip()
    if '-->' in line or line == '':
        return ''
    else:
        line = line.encode('ascii', 'ignore')
        if line.isdigit():
            return ''
        else:
            return ' '.join(line.split())


def extract_text(fn, encoding):
    '''
    extract text from srt with the encoding
    '''
    tt = []
    with io.open(fn, 'r', encoding=encoding) as g:
        lines = g.readlines()
        for x in lines:
            y = check_text(x)
            if y:
                tt.append(y)
        text = ' '.join(tt).strip()
    return text


def extract_file(fn):
    '''
    extract text from srt file
    '''
    try:
        f = open(fn)
        content = f.read()
        f.close()
        r = chardet.detect(content)
        charenc = r['encoding']
        text = extract_text(fn, charenc)
    except:
        charenc = None
        text = extract_text(fn, charenc)

    return text

def form_predict_page(lst, indices):
    '''
    construct webpage from the template
    '''
    with open('templates/predict_page.html', 'r') as f:
        return f.read() % tuple(lst + indices)

@app.route('/')
def index():
    # return '<h1> Something </h1>'
    return render_template('index.html')


UPLOAD_FOLDER = "temp/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/templates/moviepicker', methods=['GET'])
def submission():
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="/templates/predict_page" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
    '''

model = pickle.load(open('../code/all.pkl', 'rb'))

@app.route('/templates/predict_page', methods=['GET', 'POST'] )
def predict_page():
    global fsave
    # get data from request form, the key is the name you set in your form
    print 'test1'
    try:
        fl = request.files['file']
        print 'test2'
        if fl and request.method == "POST":
            fn = secure_filename(fl.filename)
            fsave = os.path.join(app.config['UPLOAD_FOLDER'], fn)
            fl.save(fsave)
    except:
        pass
    print 'test3'
    text = extract_file(fsave)
    text = ' '.join(a.tokenize(a.clean([text])[0]))
    W, ic = model.transfrom_predict([text])
    indices = list(np.argsort(W)[0][::-1][:5])
    thelist = []
    thesum = 0.
    for ind in indices:
        thelist.append("Topic " + str(ind))
        thelist.append(W[0][ind])
        thesum += W[0][ind]
    thelist.append("Others")
    thelist.append(str(W[0].sum() - thesum))
    thetuple = tuple(thelist)
    # print "the tuple " + str(len(thetuple))

    output = form_predict_page(thelist, indices)

    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)