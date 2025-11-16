from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('level-selection/', views.level_selection_view, name='level_selection'),
    path('game/<str:difficulty>/', views.game_view, name='game'),
    path('save-game-result/', views.save_game_result, name='save_game_result'),
    path('profile/', views.profile_view, name='profile'),
    path('game-history/', views.game_history_view, name='game_history'),
]
