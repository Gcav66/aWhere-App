from flask import Flask, request, jsonify, redirect, render_template
from flask.ext import excel
from AWhereCall import AWhereCall
from flask_bootstrap import Bootstrap
import pandas as pd

def create_app():
    app=Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/upload", methods=['GET','POST'])
def upload_file():
    template = 'upload.html'
    if request.method == 'POST':
	    return jsonify({"result": request.get_array(field_name='file')})
    return render_template(template)

@app.route("/download", methods=['GET'])
def download_file():
    y = AWhereCall('uKrHGgL0BwfN6QZx4RKZyIIZhNq6aP3G', 'aAzNqpcFsjLWvQDf')
    out = y.get_observations('gus_test_2')
    flat = y.flatten_observations(out)
    #return excel.make_response_from_array([[1,2], [3,4]], "csv")
    return excel.make_response_from_records(flat, "csv")

@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3,4]], "csv", filename="export_data")

'''
def get_array():
	y = AWhereCall('uKrHGgL0BwfN6QZx4RKZyIIZhNq6aP3G', 'aAzNqpcFsjLWvQDf')
	out = y.get_observations('gus_test_2')
	flat = y.flatten_observations(out)
	return flat
'''

@app.route('/observations', methods = ['GET','POST'])
def signup():
    observations = 'observations.html'
    if request.method == 'POST':
        print request.form
        #if request.form['Fields'] == 'Fields':
        if 'Create_Fields' in request.form:
            key = request.form['bkey']
            secret = request.form['bsecret']
            lat = request.form['blat']
            long = request.form['blong']
            field_id = request.form['field_id']
            farm_id = request.form['farm_id']
            y = AWhereCall(key, secret)
            fields = y.create_field(lat, long, field_id, farm_id)
            return render_template(observations, fields=fields)
        if 'BFields' in request.form:
            key = request.form['bkey']
            secret = request.form['bsecret']
            y = AWhereCall(key, secret)
            fields = y.get_fields()
            return render_template(observations, fields=fields)
        if 'Fields' in request.form:
            key = request.form['key']
            secret = request.form['secret']
            y = AWhereCall(key, secret)
            fields = y.get_fields()
            return render_template(observations, fields=fields)
        if 'Observations' in request.form:            
            key = request.form['key']
            secret = request.form['secret']
            field = request.form['field_id']
            y = AWhereCall(key, secret)
            out = y.get_observations(field)
            flat = y.flatten_observations(out)
            df = pd.DataFrame(flat)
            return render_template(observations, flat=df.to_html())
        if 'Download' in request.form:
            key = request.form['key']
            secret = request.form['secret']
            field = request.form['field_id']
            y = AWhereCall(key, secret)
            out = y.get_observations(field)
            flat = y.flatten_observations(out)
            return excel.make_response_from_records(flat, "csv")
    return render_template(observations)
	
@app.route('/fields', methods = ['GET', 'POST'])
def fields():
    fields = None
    template = 'fields.html'
    fields_out = 'fields_out.html'
    if request.method == 'POST':
        if request.form['submit'] == 'Observations':
            key = request.form['key']
            secret = request.form['secret']
            y = AWhereCall(key, secret)
            fields = y.get_fields()
            return render_template(fields_out, fields=fields)
        elif request.form['submit'] == 'Fields':
            key = request.form['key']
            secret = request.form['secret']
            y = AWhereCall(key, secret)
    return render_template(template)
	
	
	
if __name__ == "__main__":
    app.run(debug=True)
