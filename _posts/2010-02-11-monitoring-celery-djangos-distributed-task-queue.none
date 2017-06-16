---
layout: post
title: 'Monitoring Celery: Django''s Distributed Task Queue'
date: '2010-02-11T23:30:42+00:00'

---
Let's say you are using Django and want to process a heavy 

[Celery](http://celeryproject.org)

<style>
.screenshot {
margin-left: -13px;
}
</style>
 
<img src="http://www.ofbrooklyn.com/media/photos/celery_status_highres.png" class="screenshot" width="663" height="475" />

#!python
import os
from celery.task import Task
from celery.registry import tasks
from celery.utils import gen_unique_id 
from celery.backends import default_backend 
from celery.exceptions import RetryTaskError
from meta.models import SBCeleryTask

class SBTask(Task):
    abstract = True

    def run_task(self, *args, **kwargs):
        raise NotImplementedError("Tasks must define the run_task method.")
        
    def run(self, *args, **kwargs):
        # print 'Running task %s: %s' % (args, kwargs['task_id'])
        sb_task = SBCeleryTask.objects.get(task_id=kwargs['task_id'])
        sb_task.status = SBCeleryTask.INPROGRESS
        sb_task.save()
        
        task_result = self.run_task(*args, **kwargs)
    
        # print 'Success task %s: %s' % (args, kwargs['task_id'])
        sb_task.status = SBCeleryTask.COMPLETED
        sb_task.save()
        
        return task_result
                
    def on_retry(self, retval, task_id, args, kwargs):  
        # print "Retrying task %s: %s" % (task_id, retval)
        sb_task = SBCeleryTask.objects.get(task_id=task_id)
        sb_task.retries += 1
        sb_task.status = SBCeleryTask.RETRYING
        sb_task.tracebacks = "%s\n\n------------------\n\n%s" % (
            sb_task.task_meta.traceback,
            sb_task.tracebacks,
        )
        sb_task.save()

    def on_failure(self, retval, task_id, args, kwargs):  
        # print 'Failed task %s: %s' % (task_id, retval)
        sb_task = SBCeleryTask.objects.get(task_id=task_id)
        if sb_task.status != SBCeleryTask.RETRYING:
            sb_task.status = SBCeleryTask.FAILED
            sb_task.tracebacks = "%s\n\n------------------\n\n%s" % (
                sb_task.task_meta.traceback,
                sb_task.tracebacks,
            )
            sb_task.save()
    
    @classmethod
    def apply_async(self, args=None, kwargs=None, **options): 
        """Generate a task_id so that we can create the SBCeleryTask before 
        calling super().apply_async. That task_id is then passed to 
        super().apply_async and it uses that one rather than generating a 
        new one. If we call super().apply_async first, there's a race 
        condition where the task sometimes runs before the SBCeleryTask 
        is saved, which then causes problems."""
        
        if not 'task_id' in options:
            task_id = gen_unique_id()
            options['task_id'] = task_id
        else:
            task_id = options['task_id']
        sb_task, _ = SBCeleryTask.objects.get_or_create(
                        task_id=task_id, 
                        defaults={
                            'task_name': self.name,
                            'status': SBCeleryTask.QUEUED
                        })
        sb_task.save()
        task_result = super(SBTask, self).apply_async(args=args, 
                                                      kwargs=kwargs, 
                                                      **options) 
        default_backend.store_result(task_result.task_id,
                                     None,
                                     status="PENDING") 
        
        # Save again to populate sb_task.task_meta, which wasn't there 
        # when we saved above.
        sb_task.save() 
        
        return task_result
</code>

<code class="python">
import datetime
from django.db import models
from celery.models import TaskMeta
from picklefield.fields import PickledObjectField

class Quote(models.Model):
    quote = models.CharField(max_length=140)
    by = models.CharField(max_length=50)
    by_link = models.URLField()

class SBCeleryTask(models.Model):
    """Task result/status."""
    QUEUED = 'queued'
    INPROGRESS = 'inprogress'
    RETRYING = 'retrying'
    COMPLETED = 'completed'
    FAILED = 'failed'
    DELETED = 'deleted'
    STATUS_CHOICES = (
        (QUEUED, 'queued'),
        (INPROGRESS, 'inprogress'),
        (RETRYING, 'retrying'),
        (COMPLETED, 'completed'),
        (FAILED, 'failed'),
        (DELETED, 'deleted'),
    )
    
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255)
    task_meta = models.OneToOneField(TaskMeta, null=True, blank=True)
    status = models.CharField(max_length=50,
                              default=QUEUED,
                              choices=STATUS_CHOICES)
    retries = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    modified_date = models.DateTimeField(auto_now=True)
    tracebacks = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return u"<Task: %s successful: %s>" % (self.task_id, 
                                               self.task_meta.status)

    def save(self, *args, **kwargs):
        if not self.task_meta and self.task_id:
            try:
                self.task_meta = TaskMeta.objects.get(task_id=self.task_id)
            except TaskMeta.DoesNotExist:
                # Aww, this sucks. This should not be happening, 
                # but all is not lost.
                pass
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        super(SBCeleryTask, self).save(*args, **kwargs)
