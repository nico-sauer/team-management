from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Team, CustomUser
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from profiles.models import StaffProfile, AthleteProfile


ROLE_CHOICES = (
    ("Trainer", "Trainer"),
    ("Physical Therapist", "Physical Therapist"),
    ("Dietitian", "Dietitian"),
    ("Doctor", "Doctor"),
    ("Athlete", "Athlete"),
)

MANAGER_CHOICES = (("Manager", "Manager"),)


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *, current_user, **kwargs):
        super().__init__(**kwargs)
        self.current_user = current_user
        self.fields["team_id"].queryset = Team.objects.filter(
            manager=current_user)

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    team_id = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False
        )
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=False
                                   )
    new_group_name = forms.CharField(
        required=False,
        label="Create new group")
    new_team_name = forms.CharField(required=False, label="Create new team")

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "role",
            "team_id",
            "group",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get("role")
        # Team assignment
        # team_id = self.cleaned_data.get("team_id")
        group = self.cleaned_data.get("group")
        # Group.objects.get(name="Managers")
        # user.group = group
        # user.groups.add(group)
        if commit:
            user.save()
            user.groups.add(group)
            # user.group = group
            user.save()
            # Profile creation
            if role in [
                "Manager",
                "Trainer",
                "Physical Therapist",
                "Dietitian",
                "Doctor",
                "Chef",
            ]:
                StaffProfile.objects.create(
                    user=user,
                    first_name=self.cleaned_data["first_name"],
                    last_name=self.cleaned_data["last_name"],
                    role=role,
                )
            elif role == "Athlete":
                AthleteProfile.objects.create(
                    user=user,
                    first_name=self.cleaned_data["first_name"],
                    last_name=self.cleaned_data["last_name"],
                )
        return user


# A form for the first team member that register(Manager)


class FirstCustomUserCreationForm(UserCreationForm, forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    role = forms.ChoiceField(choices=MANAGER_CHOICES, required=False)
    team_name = forms.CharField(max_length=250)

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        initial="Managers",
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "team_name",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        team_name = self.cleaned_data["team_name"]

        if commit:

            role = "Manager"
            user.role = role

            if Team.objects.filter(team_name=team_name):
                raise ValidationError(
                    "The team is already exist, please enter another team"
                )
            else:
                user.save()
                # Create StaffProfile for the manager
                StaffProfile.objects.create(
                    user=user,
                    first_name=self.cleaned_data["first_name"],
                    last_name=self.cleaned_data["last_name"],
                    role=role,
                )

                team_id = Team.objects.create(team_name=team_name,
                                              manager=user)
                user.team_id = team_id
                group = Group.objects.get(name="Managers")
                user.group = group
                user.groups.add(group)
                user.save()

        # user.groups.set([group]) if we want more then one group to one user

        return user
