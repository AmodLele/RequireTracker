from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm

# <<<<<<< HEAD
#from django.forms import 

# class NewProjectForm(forms.Form):

# 	title = forms.CharField(max_length=128)
# 	description = forms.CharField(max_length=1024)
# =======
from requirements.models.project import Project
from requirements.models.story import Story

class NewProjectForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(NewProjectForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = Project
		fields = ('title', 'description')
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}
		
class StoryForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StoryForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += ' form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = Story
		fields = ('title', 'description', 'reason', 'test', 'status')
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
			'reason': forms.Textarea(attrs={'rows': 5}),
			'test': forms.Textarea(attrs={'rows': 5}),
		}
		
# >>>>>>> newfeature-be-editproject
class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		for name, field in self.fields.items():
			if field.widget.attrs.has_key('class'):
				field.widget.attrs['class'] += 'form-control'
			else:
				field.widget.attrs.update({'class':'form-control'})

	class Meta:
		model = User
		fields = ('first_name','last_name','email','username','password1','password2')

	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.is_active = False
		if commit:
			user.save()
		return user
	
class AddUserForm(forms.Form):
	users = User.objects.filter(is_active=True).order_by('id')
	username = forms.ModelChoiceField(queryset=users, empty_label=None)

# class registrationForm(forms.Form):
# 	firstName = forms.CharField(label='First Name:', max_length=100)
# 	lastName = forms.CharField(label='Last Name:', max_length=100)
# 	emailAddress=forms.CharField(label='Email Address:', max_length=100)
# 	username=forms.CharField(label='Username:', max_length=100)
# 	password=forms.CharField(label='password:', max_length=100, widget=forms.PasswordInput())
# 	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)

class AddIterationForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label='Description:', max_length=100, widget=forms.Textarea(attrs={'class':'form-control'}))
    start_date = forms.DateField(label='Start Date:', widget=SelectDateWidget(attrs={'class':'form-control'}))
    end_date = forms.DateField(label='End Date:', widget=SelectDateWidget(attrs={'class':'form-control'}))
