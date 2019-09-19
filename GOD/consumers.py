import json
import logging
from channels import Channel
from channels import Group
from channels.sessions import channel_session



log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    Group('info').add(message.reply_channel)
    print("connected!----")
    Group('info').send({
        'text': json.dumps({
            'status':"connected",
            
        })
    })

    


@channel_session
def ws_receive(message):
  
    if data:
        reply_channel = message.reply_channel.name

      
        print("hahah.reciveed")


def start_sec3(data, reply_channel):
    log.debug("job Name=%s", data['job_name'])
    # Save model to our database
    job = Job(
        name=data['job_name'],
        status="started",
    )
    job.save()

    # Start long running task here (using Celery)
    sec3_task = sec3.delay(job.id, reply_channel)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    job.celery_id = sec3_task.id
    job.save()

    # Tell client task has been started
    Channel(reply_channel).send({
        "text": json.dumps({
            "action": "started",
            "job_id": job.id,
            "job_name": job.name,
            "job_status": job.status,
        })
    })

