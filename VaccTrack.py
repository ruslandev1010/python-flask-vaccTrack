from flask import g, render_template, request, make_response, redirect, url_for, jsonify
from setup import app, _PORT,_HOST, _APP_NAME, _PATIENTS_TABLE,_MEASUREMENTS_TABLE,_PLACEHOLDER,_WAITPATIENTS_TABLE
from HIM73050 import flask_db as fdb
from login_auth import login_required
from flask import jsonify


@app.teardown_appcontext
def close_connection(exception):
    fdb.close_db()

@app.route('/index')
@app.route('/')
def root():
    return render_template('index.html')

'''
    Steps for porting v2 to v3, update routers and templates.

    1) copy measurements(ptid) router code to a NEW patients() router
    and modify its code so that it manages the patient list (allows listing, selecting patients, adding new patient, etc);
        this is similar to how multiple measurements list was managed for the ONE patient in v2 app
    2) rename the measurements(ptid) router to patient(ptid)
        and modify its code so that it will displays information about ONE patient
        and manages their measurement list;
        this is similar to how information about one measurement was managed in v2 app
        (i.e., list, select, add new measurement)
    3) update the measurement(ptid,mid) router
    and modify its code to allow for foth a patient info object and
    a measurement info object be passed along to the templates

    4) rename and modify the templates to reflect the above changes

there is no need to pass the patient argument to the routers;
there will be a patient ID and a patient_info object
'''
@app.route('/roster')
@login_required
def display_roster():
    patients = fdb.query_db_get_all('SELECT * FROM '+_PATIENTS_TABLE)
    waitPatients = fdb.query_db_get_all("SELECT * FROM "+_WAITPATIENTS_TABLE)
    return render_template('roster.html', patients=patients, waitPatients=waitPatients)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/patient_select')
@login_required
def select_patient():
    return render_template('patient_selector.html')

@app.route('/preschedule', methods=['GET'])
@login_required
def preSchedule():
    return render_template('pre-schedule.html')

@app.route('/wait-patients',methods=['GET', 'POST'])
@login_required
def waitPatients():
    if request.method == 'GET':
        waitPatients = fdb.query_db_get_all("SELECT * FROM "+_WAITPATIENTS_TABLE)
        return redirect(url_for('preSchedule'))
    elif request.method == 'POST':
        name = request.form['name1']
        date = request.form['date1']
        healthcard = request.form['healthcard1']
        email = request.form['email1']
        vaccinetype = request.form['vaccinetype1']
        estimatetime = request.form['estimateTime']
        result=fdb.query_db_change('INSERT INTO '+_WAITPATIENTS_TABLE+'(name, dob, healthcard, email, vaccinetype, estimatetime) VALUES ({0}, {0}, {0}, {0}, {0}, {0})'.format(_PLACEHOLDER),(name, date, healthcard, email, vaccinetype, estimatetime))
        if result==None:
            print("Could not insert new record into",_WAITPATIENTS_TABLE)
        return redirect(url_for('preSchedule'))

@app.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    search = request.args.get('q')
    query = 'SELECT * FROM '+_PATIENTS_TABLE + ' WHERE firstname LIKE %s OR lastname LIKE %s'
    args = ('%' + search + '%', '%' + search + '%')
    patient_list = fdb.query_db_get_all(query, args)
    # return jsonify(patient_list)
    patients = []
    for patient in patient_list:
        name = patient["firstname"] + " " + patient["lastname"]
        patients.append(name)
    # for (i = 0; i < patient_list.length; i++) {

    # }
    return jsonify(patients)

@app.route('/patients',methods=['GET', 'POST'])
@login_required
def patients():
    '''Works'''
    if request.method == 'GET':
        patient_list = fdb.query_db_get_all("SELECT * FROM "+_PATIENTS_TABLE)
        #return "OK"
        #return patient_list
       # return render_template('roster.html', patients=patient_list)
        #print(patient_list)
        return jsonify(patient_list)
    elif request.method == 'POST':
        fName = request.form['first_name']
        lName = request.form['last_name']
        email = request.form['e_mail']
        tmp = False
        result=fdb.query_db_change('INSERT INTO '+_PATIENTS_TABLE+'(firstname, lastname, email, firstdose, seconddose, thirddose) VALUES ({0}, {0}, {0}, {0}, {0}, {0})'.format(_PLACEHOLDER),(fName, lName, email, tmp, tmp, tmp))
        if result==None:
            print("Could not insert new record into",_PATIENTS_TABLE)
        return redirect(url_for('select_patient'))

@app.route('/patient/<int:ptid>/'+_APP_NAME, methods=['GET', 'POST'])
@login_required
def patient(ptid):
    '''Works '''
    if request.method == 'GET':
        patient_info = fdb.query_db_get_one('SELECT * FROM '+_PATIENTS_TABLE+' WHERE id={0}'.format(_PLACEHOLDER),(ptid,))
        #retrieve measurements
        #query='SELECT * FROM '+_MEASUREMENTS_TABLE+' WHERE patient_id={0}'.format(_PLACEHOLDER) # this IS good enough@
        #no need to join - keeping the patient and measurements dictionary separate, makes it easier/more intuitive to write the template code
        #query='SELECT * FROM '+_MEASUREMENTS_TABLE+' as v JOIN (SELECT * FROM Patients WHERE id={0}) as p ON v.patient_id=p.id'.format(_PLACEHOLDER)
        #patient_measurements = fdb.query_db_get_all(query,(ptid,))
        #return render_template('patient.html', patient=patient_info, measurements=patient_measurements)
        return render_template('patient.html', patient=patient_info)

    elif request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        firstdose = request.form['firstdose']
        seconddose = request.form['seconddose']
        thirddose = request.form['thirddose']
        query = 'UPDATE patients SET firstname=%s, lastname=%s, email=%s, firstdose=%s, seconddose=%s, thirddose=%s WHERE id=%s'
        args = (firstname, lastname, email, firstdose, seconddose, thirddose, ptid)

        fdb.query_db_change(query, args)
        return redirect(url_for('patient',ptid=ptid))

@app.route('/patient/<ptid>/'+_APP_NAME+'/measurement/<mid>')
@login_required
def measurement(ptid,mid):
    patient_info = fdb.query_db_get_one('SELECT * FROM '+_PATIENTS_TABLE+' WHERE id={0}'.format(_PLACEHOLDER),(ptid,))
    pt_msmt=fdb.query_db_get_one('SELECT id, systolic, diastolic, pulse, time_recorded FROM '+_MEASUREMENTS_TABLE+' WHERE id = {0}'.format(_PLACEHOLDER), (mid,))
    return render_template('measurement.html',patient=patient_info, measurement=pt_msmt)

if __name__ == '__main__':
    app.debug = True
    app.run(port=_PORT, host=_HOST)

