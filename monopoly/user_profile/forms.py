from django import forms
from django.core.exceptions import ValidationError
from .models import SupportTicket

class CommentaryForm(forms.Form):
    comment = forms.CharField(min_length=4, max_length=512)

    def clean_comment(self):
        data = self.cleaned_data["comment"]
        if "communism" in data.lower():
            self.add_error("comment", "You used prohibited words.")

class SupportTicketForm(forms.ModelForm):
    assignee = forms.CharField(min_length=5, max_length=100, required=False)
    email = forms.CharField(required=False)

    class Meta:
        model = SupportTicket
        fields = ['message', 'title']

    def clean_assignee(self):
        data = self.cleaned_data.get("assignee").split(" ")
        if not data[0]:
            return 

        if len(data) < 2:
            self.add_error("assignee", "Please, enter your real name.")
            return self.cleaned_data.get("assignee")

        for word in data:
            if list(word)[0] == list(word)[0].lower():
                self.add_error("assignee", "Please, enter your real name.")
                return self.cleaned_data.get("assignee")

        for num in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
            if str(num) in data:
                self.add_error("assignee", "Please, enter your real name.")
                return self.cleaned_data.get("assignee")

        return self.cleaned_data.get("assignee")
    

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return None
        if len(email.split("@")) != 2:
            self.add_error("email", "You entered invalid email.")
        return self.cleaned_data.get("email")
        

    def clean_message(self):
        message = self.cleaned_data["message"].split(" ")
        if len(message) <= 10:
            self.add_error("message", "Please, provide more verbose explanation of the issue.")
        return self.cleaned_data.get("message")

    def clean(self):
        cleaned_data = super().clean()
        
        if (cleaned_data["assignee"] and not cleaned_data["email"] or \
        not cleaned_data["assignee"] and cleaned_data["email"]) and not \
        (self.has_error("assignee") or self.has_error("email")):
            self.add_error("assignee", "Please, provide both your name and email if you want to leave your credentials.")
        