from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project
from iteration import Iteration

class Story(ProjMgmtBase):
    STATUS_UNSTARTED = 1
    STATUS_STARTED = 2
    STATUS_COMPLETED = 3
    STATUS_ACCEPTED = 4

    STATUS_CHOICES = (
        (STATUS_UNSTARTED, "Unstarted"),
        (STATUS_STARTED, "Started"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ACCEPTED, "Accepted")
    )
    
    POINTS_NONE = 0
    POINTS_ONE = 1
    POINTS_TWO = 2
    POINTS_THREE = 3
    POINTS_FOUR = 4
    
    POINTS_CHOICES = (
        (POINTS_NONE,"0 Not Scaled"),
        (POINTS_ONE, "1 Point"),
        (POINTS_TWO, "2 Points"),
        (POINTS_THREE, "3 Points"),
        (POINTS_FOUR, "4 Points")
    )

    project = models.ForeignKey(Project)    
    iteration = models.ForeignKey(Iteration,blank=True,null=True)
    reason = models.CharField(default='', max_length=1024,blank=True)
    test= models.CharField(default='', max_length=1024, blank=True)
    hours = models.CharField(default='', max_length=16, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, max_length=1, default=STATUS_UNSTARTED)
    points = models.IntegerField(choices=POINTS_CHOICES, max_length=1, default=POINTS_NONE)
    pause = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.title

    def description_as_list(self):
        return self.description.split('\n')

    def reason_as_list(self):
        return self.reason.split('\n')

    def test_as_list(self):
        return self.test.split('\n')
        
    class Meta:
        app_label = 'requirements'
    
def get_project_stories(projID):
    return Story.objects.filter(project_id=projID)

def get_story(storyID):
    try:
        return Story.objects.get(id=storyID)
    except Exception, e:
        return None
    
    
def create_story(user, proj, fields):
    if proj is None: return None
    if Project.objects.filter(id=proj.id).count() == 0: return None
    if fields is None: return None
    
    title = fields.get('title', '')
    description = fields.get('description', '')
    reason = fields.get('reason', '')
    test = fields.get('test', '')
    hours = fields.get('hours','')
    status = fields.get('status', Story.STATUS_UNSTARTED)
    points = fields.get('points',Story.POINTS_NONE)
    pause = fields.get('pause',False)
    
    story = Story(project=proj,
                  title=title, 
                  description=description,
                  reason=reason,
                  test=test,
                  hours = hours,
                  status=status,
                  points = points,
                  pause = pause
                  )
    story.save()
    return story

def delete_story(storyID):
    story = Story.objects.filter(id=storyID)
    story.delete()
