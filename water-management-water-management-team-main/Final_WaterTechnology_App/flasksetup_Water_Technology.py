from flask import Flask, render_template, url_for, request
import os
#from RandomforestModel import Randomforest
#from Predictions_pH import phPredictionFucnt
from CombinedPredictions import combine_predictions
#import sys sys.path.append('D:/Case_study/CaseStudy_app/new file/new file/')

#from Prediction import your_function  # Replace 'your_function' with the actual function or object you want to import
#from application.app.folder.file import func_name
#from River_Code.Data_ingestion_and_cleaning import correct_column_names

#from "new_file/new_file/Prediction"  import correct_column_names
from new_file.new_file.PredictionWithWQI import river_prediction
import  new_file.new_file.WQI 




app = Flask(__name__)

picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

posts = [{'author': 'kartikeya', 'title': 'Student'},
         {'project': 'Water Technology', 'University': 'SRH'}]

# Define a default value for finuse
default_finuse = {}
default_finuse2 = []
default_finuse3 = {}
default_finuse4 = []

@app.route("/", methods=["POST"])
@app.route("/home")
def getvalue():
    lst1 = []
    usenum = request.form["UseCase"]
    stationname = request.form["StationType"]
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-998408412-612x612.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1176776516-612x612.jpg')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1140109092-612x612.jpg')
    pic4 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1011436592-612x612.jpg')
    print(usenum)
    print(stationname)
    
    usercasenumberoutput,datelist = combine_predictions(usenum)
    usercasenumberoutputriver,datelistriver = river_prediction(stationname)
    print(usercasenumberoutput)
    return render_template('home.html', selected_station=stationname, usecase=usenum,
                           posts=posts, user_image=pic1, user_image2=pic2, user_image3=pic3,
                           user_image4=pic4, finuse=usercasenumberoutput, finuse2 = datelist, finuse3=usercasenumberoutputriver, finuse4=datelistriver)

@app.route("/")
@app.route("/home")  
def home():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-998408412-612x612.jpg')
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1176776516-612x612.jpg')
    pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1140109092-612x612.jpg')
    pic4 = os.path.join(app.config['UPLOAD_FOLDER'], 'istockphoto-1011436592-612x612.jpg')
    
    # Use the default value for finuse if not defined yet
    return render_template('home.html', posts=posts, user_image=pic1, user_image2=pic2, user_image3=pic3, user_image4=pic4, finuse=default_finuse, finuse2=default_finuse2,finuse3=default_finuse3, finuse4=default_finuse4)

if __name__ == "__main__":
    app.run(debug=True)
