
# Register your models here.
from django.contrib import admin
from .models import User, Book

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_approved')
    actions = ['approve_users', 'disapprove_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    def disapprove_users(self, request, queryset):
        queryset.update(is_approved=False)

    approve_users.short_description = "Approve selected users"
    disapprove_users.short_description = "Disapprove selected users"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'upload_date', 'expiry_date')