from django import forms
from .models import *
from django.db.models.functions import Lower
from django.forms import ModelChoiceField, ChoiceField


all_groups = Student.objects.order_by('group').values_list('group').distinct().all()
group_choice_list = [[group[0], f'Group: {group[0]}'] for group in all_groups]
group_choice_list.insert(0, ['', 'No group choice'])


class StudentModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'Group: {obj.group}; Name: {obj.real_name}; ID: {obj.id}'


class SendPollForm(forms.ModelForm):
    error_css_class = 'form-errors'
    
    group = ChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        choices=group_choice_list,
        label='Group',
        required=False)
    
    student = StudentModelChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        queryset=Student.objects.all().order_by('group', Lower('real_name')),
        label='Student', empty_label='No student choice',
        required=False)
    
    open_period = forms.IntegerField(
        required=False, min_value=0, max_value=600,
        widget=forms.TextInput(attrs={
            'placeholder': 'Open period (integer up to 600 seconds)...',
            'class': 'option-input'
        })
    )
    
    option0 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 0 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_0 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option1 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 1 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_1 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option2 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 2 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_2 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option3 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 3 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_3 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option4 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 4 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option5 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 5 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_5 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option6 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 6 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_6 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option7 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 7 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_7 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option8 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 8 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_8 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    option9 = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type option 9 here (up to 100 characters)...',
            'class': 'option-input'
        })
    )
    
    is_correct_9 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'correct-checkbox'}
        )
    )
    
    class Meta:
        model = TelegramPoll
        fields = ['question']
        widgets = {
            'question': forms.Textarea(
                attrs={
                    'placeholder': 'Type poll question here (up tp 300 characters)...',
                    'class': 'message-input'
                }
            )
        }


class SendQuestionForm(forms.ModelForm):
    error_css_class = 'form-errors'
    
    group = ChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        choices=group_choice_list,
        label='Group',
        required=False)
    
    student = StudentModelChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        queryset=Student.objects.all().order_by('group', Lower('real_name')),
        label='Student', empty_label='No student choice',
        required=False)
    
    class Meta:
        model = TelegramMessage
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Type your question here (up to 4096 characters)...',
                    'class': 'message-input'
                }
            )
        }


class SendMessageForm(forms.Form):
    error_css_class = 'form-errors'
    
    msg_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'Type your message here (up to 4096 characters)...',
            'class': 'message-input'
        }), max_length=4096)
    
    group = ChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        choices=group_choice_list,
        label='Group',
        required=False)
    
    student = StudentModelChoiceField(
        widget=forms.Select(attrs={'class': 'select-input'}),
        queryset=Student.objects.all().order_by('group', Lower('real_name')),
        label='Student', empty_label='No student choice',
        required=False)
