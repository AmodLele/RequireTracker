from django.test import TestCase
import models.project
from models.project import Project
import models.project_api
from models.user_association import UserAssociation
from django.contrib.auth.models import User
import models.user_manager

class Obj(): pass
    

class ProjectTestCase(TestCase):
    
    def setUp(self):
        self.__clear()
        
        self.__user = User(username="testUser", password="pass")
        self.__user.save()
        
    def tearDown(self):
        self.__clear()
        
    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete
        
    def test_getAllProjects_none(self):
        self.assertEqual( models.project_api.get_all_projects().count(), 0)
        
    def test_getAllProjects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_all_projects().count(), 1)

    def test_getAllProjects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        p2 = Project(title="title2", description="desc2")
        p2.save()
        
        self.assertEqual( models.project_api.get_all_projects().count(), 2)
        
    def test_getAllProjectsForUser_none(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 0)
        
    def test_getAllProjectsForUser_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 1)    
    
    def test_canUserAccessProject_cant(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), False)    
        
    def test_canUserAccessProject_can(self):
        p = Project(title="title", description="desc")
        p.save()
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), True)        
    
    def test_createUser(self):
        req = Obj()
        req.POST = {'username' : 'user', 'password' : 'pass'}
        models.user_manager.createUser(req)
        
        u = User.objects.all()[1]
        self.assertEqual('user', u.username)
        self.assertEqual(False, u.is_active)