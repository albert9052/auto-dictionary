from flask import Flask, jsonify, render_template, request, send_file, send_from_directory
from threading import Thread
import time
import wordsToDocx
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

threadExist = False
fileName = 'temp.docx'
progress = {'finished' : 0, 'total' : 0, 'finishedAllTheWork' : True}

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return r

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods = ['POST'])
def upload():
    
    global threadExist
    global fileName
    global progress

    if threadExist:
        thread.terminate()
    dicName = 'C:\\Users\\User\\OneDrive\\Documents\\文林心相關\\詳解\\詳解需求\\字典.txt'
    words = request.form['words']
    if words == '':
        return {'error' : 'missing words'}
        
    dic = wordsToDocx.getDic(dicName)
    listOfWords = words.split('\n')
    for i in range(0, len(listOfWords)):
        if listOfWords[i] == '':
            listOfWords[i] = '\n'
    progress['finished'] = 0
    progress['total'] = 0
    def startMakingDocx():
        threadExist = True
        progress['finishedAllTheWork'] = False
        wordsToDocx.makeVocWord(dic, listOfWords, fileName, progress)
    thread = Thread(target = startMakingDocx)
    thread.start()
    return {}

@app.route('/download', methods = ['GET'])
def download():
    
    directory = os.getcwd()
    return send_from_directory(directory, fileName, as_attachment=True, cache_timeout=0)
    
@app.route('/checkProgress', methods = ['POST'])
def checkProgress():

    global progress
    print(progress)
    return jsonify(progress)

app.run(host = '0.0.0.0', port = '9000')