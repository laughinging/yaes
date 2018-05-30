import logging
from flask import Flask, request, make_response, jsonify, render_template, Response
from set_up import redis_conn, mail_queue
from backend.send import send_mail

from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError

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
        form = request.form
        sender = form.get('sender')
        recipient = form.get('recipient')  
        subject = form.get('subject')
        body = form.get('body')

        try:
            job = mail_queue.enqueue(send_mail, 
                    sender=sender, recipient=recipient,
                        subject=subject, body=body
                    )
            message = 'Add task to queue successfully'
            app.logger.info(message)
            return jsonify(
                    {
                        'status': 'submitted', 
                        'info': message, 
                        'job_id': job.get_id(), 
                        'status_code': 200
                        }
                    )

        except: 
            message = 'Connection to Redis failed.'
            app.logger.error(message)
            return jsonify(
                    {
                        'status': 'fail', 
                        'error': 'Service not available, try later.', 
                        'status_code': 500
                        }
                    )
        
    return render_template('index.html')


@app.route('/check', methods=['POST', 'GET'])
def get_job_status():

    if request.method == 'POST':
        job_id = request.form.get('job_id')

        try:
            job = Job.fetch(job_id, connection=redis_conn)

        except NoSuchJobError:
            message = 'Invalid job id.'
            app.logger.info(message)
            return jsonify(
                    {
                        'status': 'fail',
                        'info': message,
                        'status_code': 400,
                        }
                    )

        except Exception:
            message = 'Connection to Redis failed.'
            app.logger.error(message)
            return jsonify(
                    {
                        'status': 'fail', 
                        'info': 'Checking service not available, try later.', 
                        'status_code': 501
                        }
                    )


        app.logger.info('check job {}'.format(job_id))
        if job.is_finished:
            return jsonify(
                    {
                        'job_id': job_id, 
                        'status': 'finished', 
                        'info': 'Email sent successfully.',
                        'status_code': 200
                        }
                    )

        elif job.is_queued:
            return jsonify(
                    {
                        'job_id': job_id, 
                        'status': 'waiting',
                        'info': 'Job in queue, check status later.',
                        'status_code': 201
                        }
                    )

        elif job.is_started:
            return jsonify(
                    {
                        'job_id': job_id, 
                        'status': 'started',
                        'info': 'Email being sent, check status later.',
                        'status_code': 202
                        }
                    )
        elif job.is_failed:
            exc_info = job.exc_info
            message = exc_info.split('\n')[-2].split(': ')[-1]
            return jsonify(
                    {
                        'job_id': job_id, 
                        'status': 'failed',
                        'info': message,
                        'status_code': 203,
                        }
                    )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


