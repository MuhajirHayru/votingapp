# voting/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Candidate

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('university_id', 'first_name', 'last_name', 'department', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'department')
    fieldsets = (
        (None, {'fields': ('university_id', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'department')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('university_id', 'first_name', 'last_name', 'department', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('university_id',)
    ordering = ('university_id',)

# ✅ Use correct field name 'full_name'
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vote_count')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Candidate, CandidateAdmin)
