from django import forms
from django.core.exceptions import ValidationError
from .models import SupportTicket
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate

prohibited_words = {"communism", "ussr"}


class CommentaryForm(forms.Form):
    comment = forms.CharField(min_length=4, max_length=512)

    def clean_comment(self):
        data = self.cleaned_data["comment"]

        for word in prohibited_words:
            if word in data.lower():
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
            # If there are less than 2 words
            raise ValidationError("Please, enter your real name.")

        for word in data:
            # If some word starts with lowercase
            if list(word)[0] == list(word)[0].lower():
                raise ValidationError("Please, enter your real name.")

        for num in range(10):
            # If there are number in the name
            if str(num) in data:
                raise ValidationError("Please, enter your real name.")

        return self.cleaned_data.get("assignee")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return None

        if len(email.split("@")) != 2:
            # If '@' char doesn't split email in two pieces (you@gmail.com)
            self.add_error("email", "You entered invalid email.")
        return self.cleaned_data.get("email")

    def clean_message(self):
        message = self.cleaned_data["message"].split(" ")

        if len(message) <= 10:
            self.add_error("message", "Please, provide more verbose explanation of the issue.")
        return self.cleaned_data.get("message")

    def clean(self):
        cleaned_data = super().clean()

        if (cleaned_data["assignee"] and not cleaned_data["email"] or
                not cleaned_data["assignee"] and cleaned_data["email"]) and not \
                (self.has_error("assignee") or self.has_error("email")):
            # If one of assignee and email fields is empty and it's not due to them failing validation previously:
            self.add_error("assignee", "Please, provide both your name and email \
                            if you want to leave your credentials.")


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=24, required=True)
    password = forms.CharField(min_length=8, max_length=128, required=True)

    def clean_username(self):
        data = self.cleaned_data["username"]

        if AuthUser.objects.filter(username=data):
            raise ValidationError("The username is already taken!")

        if ' ' in data:
            raise ValidationError("Your username cannot have spaces in it!")

        return data

    def clean_password(self):
        data = self.cleaned_data["password"]

        error = True
        for char in range(10):
            if str(char) in data:
                error = False
                break
        if error:
            raise ValidationError("Your password must contain numbers!")

        if ' ' in data:
            raise ValidationError("Your password cannot have spaces in it!")

        return data

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("username") and cleaned_data.get("password"):
            if cleaned_data.get("username").lower() in cleaned_data.get("password").lower():
                raise ValidationError("You can't include you username into the password!")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=24, required=True)
    password = forms.CharField(max_length=250, required=True)

    def clean(self):
        cleaned_data = super().clean()

        authenticate(username=cleaned_data.get('username'))

        return cleaned_data


class BioForm(forms.Form):
    bio = forms.CharField(max_length=512)

    def clean_bio(self):
        data = self.cleaned_data["bio"]

        for word in prohibited_words:
            if word in data.lower():
                raise ValidationError("You used prohibited words.")
