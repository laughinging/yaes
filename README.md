# yaes - yet another email server 
Implementation for [Uber coding challenge - Email
server](https://github.com/uber/coding-challenge-tools/blob/master/coding_challenge.md)

Service available at [35.204.58.232:8888](http://35.204.58.232:8888/)

## Content

* [Overview](#overview)
* [Quick start](#quick-start)
   * [Use the email service](#use-the-email-service)
   * [Set up your own yaes](#set-up-your-own-yaes)
      * [Requirements](#requirements)
      * [Start yaes](#start-yaes)
      * [Monitor](#monitor)
* [Design](#design)
   * [Job and Worker](#job-and-worker)
      * [Send email](#send-email)
      * [Update provider pool](#update-provider-pool)
   * [Queue](#queue)
* [Test](#test)
* [If I had more time, I would have ...](#if-i-had-more-time-i-would-have-)
* [About the project](#about-the-project)

## Overview 
yaes accepts email information from clients and sends emails. yaes uses multiple
email service provider as backends. If one of the providers goes down, email
requests are passed to remaining providers without affecting clients.

- **Reliability:** Valid email could be sent eventually until there is no email
  provider available.  The controller of yaes is composed of processing queue,
  failed queue and a provider pool.  If an email is rejected due to temporary
  server error, it is stored in the failed queue and can be handled later. All
  providers in the pool are verified by timed verification job.  A provider will
  be removed if the verification fails.

- **Separation:** The frontend and backend of yaes are separated. The communication
  between frontend and backend is json-style post request. A webpage is provided
  to generate and to verify this request.  

- **Highspeed:** yaes is designed and implemented based on producer-consumer model.
  Each provider in the pool takes tasks when it is free.  Various providers can
  be potentially added into the pool so that tasks are processed parallelly,
  which significantly improves processing speed. 

- **Availability:** Clients can submit tasks directly on the website or use json
  requests. The task queue can be monitored with command line tools or a
  dashboard in browser.

- **Flexibility:** If one server provider is currently unavailable, it is removed
  from the provider pool. The add and remove API of provider pool are provided
  as well.


## Quick start

### Use the email service

The Web Frontend provides two functions ```submit email task``` and ```check
job status```. For submitting, simply fill in the contents and submit. Valid email will
be added to the task queue and wait to be sent. A job id is returned on the Web
Frontend for tracking the job status.

The functions can be accessed with HTTP POST request. See
```frontend/client.py``` as an example.

**submit email task**

```POST / ```
```
{
    sender,
    recipient,
    subject,
    body
}
```
The HTTP POST request will return one of the following status:
```
200: Email add to queue successfully.
500: Service not available.
```

**check job status**

```POST /check ```
```
{
    job_id
}
```
The HTTP POST request will return one of the following status:
```
200: job finished
201: job in queue
202: job being processed
203: job failed 
400: invalid job id
501: checking service not available
```


### Set up your own yaes

#### Requirements
yaes uses [Flask](http://flask.pocoo.org/) for web app,
[redis](https://redis.io/) as in-memory database, [rq](http://python-rq.org/) to
handle task queue.  [rq-dashboard](https://github.com/eoranged/rq-dashboard) is
recommended to view task queue status.  I use [gunicorn](http://gunicorn.org/)
to deploy the web app on [Google Cloud Computer Engine](https://cloud.google.com/compute/)

By default, yaes uses [SendGrid](https://sendgrid.com/) and
[Mailgun](https://www.mailgun.com/) as email service provider. Thus api key for
those services are required. Remember to set environment variable
```SENDGRID_API_KEY``` and ```MAILGUN_API_KEY```.

#### Start yaes

- start redis server
```
redis-server
```

- check settings (redis server, API_KEY, default server provider...) 
```
python set_up.py
```

- start web app (provider)
```
python frontend/app.py
```

- start worker (consumer)
```
python backend/worker.py
```

#### Monitor 
rq-dashboard is a web frontend to monitor redis queue, jobs and workers. Simply
start with:
```
rq-dashboard

```

The available providers are stored in redis as ```provider_pool```. 




## Design

yaes is a typical provider-consumer application. The Web frontend takes into
email tasks and stores in redis queue, as the job provider. The backend workers
get jobs from the redis queue and call corresponding functions to finish the
task, as the job consumer. Other tasks can also be queued in this system. For
example, manually update email provider pool.

### Job and Worker
#### Send email
Email jobs are generated from frontend client. The module ```send_mail``` takes
jobs from the redis queue. Each time, yaes looks up ```provider_pool``` for
available service providers and applies the task. If a job fails due to a
service provider error, the service provider is temperarily removed from
provider pool. The worker then tries remaining service provider(s) for the job.
Job with client error (malformed emails, missing items...) won't go through all
the service providers. It raises client error immediately.  If a job fails, the
job is marked with error information (client error, server error) and stored in
the failed queue. The jobs can be further handled according to the error
information. Check sudo code below.

```
def send_mail(*args, **kwargs):
    get provider_pool

    sent = False
    for provider in provider_pool:
        try:
            use provider to send mail
            sent = True
            break

        except ClientError as e:
            raise InvalidRequestError(e.description) 

        except ProviderServerError:
            provider_updating_queue.enqueue(remove_provider, provider_name)

    if not sent:
        raise ServerError
```

Send_mail returns one of the following results.
```
success 
400: failed with ClientError
500: failed with ServerError
```

#### Update provider pool
Consider the real-world case, one of the service provider is temperarily not
available because your account is out of balance. The provider is automatically
removed from the provider pool. Once you resolve the balance problem, you can
quickly update the provider pool using ```update_provider_pool```.
```
usage: update_provider_pool.py [-h] [-r [R [R ...]]] [-a [A [A ...]]]

Manually update available providers

optional arguments:
  -h, --help      show this help message and exit
  -r [R [R ...]]  provider list to remove
  -a [A [A ...]]  provider list to add
```


### Queue
yaes listens to two task queues with different priorities. 

- send mail (default)
- update provide pool (high)

As for a real world application, it is possible to intergrate other tasks.

## Test
Tests are implemented for most of the units. Check ```test_*.py``` files for
details. Briefly, I have checked the following cases.

frontend

 * invalid email address - rejcted immediately before add to the task queue

backend

 * redis server fails - raise server error
 * no available provides - raise server error 
 * bad email request - raise client error for clients
 * email not sent due to provider issues - raise server error for clients, 
 raise service provider error for backend users.


## If I had more time, I would have ...

- **automatically check mail format** 
Now all the HTTP POST requests are submitted to the task queue and later
processes by at least one service provider. It would be efficient if malformed
emails can be filtered out at the very beginning. Currently, I only use an 'email'
label in `index.html` to check wether the email address is valid.

- **automatically add/remove service provider**
It is possible to use timed varification to check the service provider status
and add/remove automatically.

- **atomatically deal with failed jobs**
The failed jobs are stored in a 'failed' queue with error type. It is possible
to deal with these jobs according to their error types, i.e, re-try those jobs
that are failed due to temperary server errors, discard those with client errors.

## About the project

- Backend track (with minimal frontend)
- Python (fluent)
- Flask, Redis(limited knowledge and experience)
- Google cloud (experienced)


