from django.contrib import admin
from .models import UserProfile, Game, GameStatistics


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['user', 'difficulty', 'result', 'time_taken', 'attempts_used', 'created_at']
    list_filter = ['difficulty', 'result', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(GameStatistics)
class GameStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_games', 'total_wins', 'total_losses', 'average_time', 'most_played_level', 'last_updated']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']
