from django.contrib import admin

from candidate_tests import models


@admin.register(models.TestingSession)
class TestingSessionAdmin(admin.ModelAdmin):
    ordering = ('created',)
    search_fields = ('candidate',)
    list_display = ('candidate', 'created')
    readonly_fields = ('created',)


@admin.register(models.TestingSessionToken)
class TestingSessionTokenAdmin(admin.ModelAdmin):
    list_display = ('session', 'key')


@admin.register(models.TestingSessionState)
class TestingSessionStateAdmin(admin.ModelAdmin):
    list_display = ('session', 'state')


@admin.register(models.TestAmount)
class TestAmountAdmin(admin.ModelAdmin):
    list_display = ('candidate_creator', 'test', 'amount')


@admin.register(models.TestingSessionTest)
class TestingSessionTestAdmin(admin.ModelAdmin):
    list_display = ('session', 'name', 'status')
