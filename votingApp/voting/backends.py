# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class UniversityIDBackend(ModelBackend):
    def authenticate(self, request, university_id=None, password=None, **kwargs):
        if university_id is None or password is None:
            return None
        try:
            user = CustomUser.objects.get(university_id=university_id)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
