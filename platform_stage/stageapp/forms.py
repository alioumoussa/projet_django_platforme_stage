from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth

from stageapp.models import *
from ckeditor.widgets import CKEditorWidget


    

class StageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Stage Title :"
        self.fields['location'].label = "Stage Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Stage Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Nouakchott',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': 'Compensation',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: Python, JavaScript ',
            }
        )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
                
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    


    class Meta:
        model = Stage

        fields = [
            "title",
            "location",
            "stage_type",
            "category",
            "salary",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_stage_type(self):
        stage_type = self.cleaned_data.get('stage_type')

        if not stage_type:
            raise forms.ValidationError("Service is required")
        return stage_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("category is required")
        return category


    def save(self, commit=True):
        stage = super(StageForm, self).save(commit=False)
        if commit:
            
            stage.save()
        return stage




class JobApplyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['stage']

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkJob
        fields = ['stage']




class JobEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Stage Title :"
        self.fields['location'].label = "Stage Location :"
        self.fields['salary'].label = "Salary :"
        self.fields['description'].label = "Stage Description :"
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Software Developer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Nouakchott',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': 'compansation',
            }
        )
        # self.fields['tags'].widget.attrs.update(
        #     {
        #         'placeholder': 'Use comma separated. eg: Python, JavaScript ',
        #     }
        # )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    

    
        last_date = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': 'Service Name',
                    'class' : 'datetimepicker1'
                }))

    class Meta:
        model = Stage

        fields = [
            "title",
            "location",
            "stage_type",
            "category",
            "salary",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_stage_type(self):
        stage_type = self.cleaned_data.get('stage_type')

        if not stage_type:
            raise forms.ValidationError("Stage Type is required")
        return stage_type

    def clean_category(self):
        category = self.cleaned_data.get('category')

        if not category:
            raise forms.ValidationError("Category is required")
        return category


    def save(self, commit=True):
        stage = super(JobEditForm, self).save(commit=False)
      
        if commit:
            stage.save()
        return stage

