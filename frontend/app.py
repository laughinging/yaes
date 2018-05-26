import logging
from flask import Flask, request, make_response, json, render_template
from set_up import redis_conn, mail_queue
from backend.send import send_mail

from rq import Queue
from rq.job import Job
from worker import send_mail, conn
from wtforms import Form, TextField

class SubmitForm(Form):
    sender = TextField('From')
    recipient = TextField('To')
    subject = TextField('Subject')
    body = TextField('Body')

app = Flask(__name__)

# logging configuration
handler = logging.FileHandler('app.log')
logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route('/', methods=['GET', 'POST'])
def get_request():

    if request.method == 'POST':
        #form: from_email, to_email, subject, body
        form = SubmitForm(request.form)
        sender = form.sender.data
        recipient = form.recipient.data
        subject = form.subject.data
        body = form.body.data

        try:
            job = mail_queue.enqueue(send_mail, args=(sender, recipient, subject,
                body,))
            message = 'Add task to queue successfully'
            app.logger.info(message)
            return make_response(json.dumps({'status': 'submitted', 
                'info': message, 'job_id': job.get_id()}), "200", {})
            #return render_template('check.html')

        except: 
            message = 'Connection to Redis failed.'
            app.logger.error(message)
            return make_response(json.dumps({'status': 'fail', 
                'error': 'Service down'}), '500', {})
        
    return render_template('index.html')


@app.route('/check/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job = Job.fetch(job_id, connection=conn)
    app.logger.info('check job {}'.format(job_id))

    if job.is_finished:
        return make_response(json.dumps({'job_id': job_id, 'status':
            'finished'}), '200', {})
    else:
        
        return make_response(json.dumps({'job_id': job_id, 'status':
            'waiting'}), '200', {})

if __name__ == '__main__':
    app.run(debug=True)


