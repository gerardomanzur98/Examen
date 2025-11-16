from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
import json
from .models import UserProfile, Game, GameStatistics


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('level_selection')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'memory_game/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'memory_game/register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'memory_game/register.html')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
            return render(request, 'memory_game/register.html')
        
        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'memory_game/register.html')
        
        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            # Create profile
            UserProfile.objects.create(user=user)
            # Create statistics
            GameStatistics.objects.create(user=user)
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'memory_game/register.html')
    
    return render(request, 'memory_game/register.html')


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('level_selection')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'memory_game/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('level_selection')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'memory_game/login.html')
    
    return render(request, 'memory_game/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def level_selection_view(request):
    """Level selection view"""
    return render(request, 'memory_game/level_selection.html')


@login_required
def game_view(request, difficulty):
    """Main game view"""
    valid_difficulties = ['basic', 'medium', 'advanced']
    
    if difficulty not in valid_difficulties:
        messages.error(request, 'Invalid difficulty level.')
        return redirect('level_selection')
    
    config = Game.get_difficulty_config(difficulty)
    
    context = {
        'difficulty': difficulty,
        'max_attempts': config['attempts'],
        'time_limit': config['time_limit']
    }
    
    return render(request, 'memory_game/game.html', context)


@login_required
@require_POST
def save_game_result(request):
    """Save game result via AJAX"""
    try:
        data = json.loads(request.body)
        
        difficulty = data.get('difficulty')
        result = data.get('result')
        time_taken = float(data.get('time_taken', 0))
        attempts_used = int(data.get('attempts_used', 0))
        
        config = Game.get_difficulty_config(difficulty)
        
        # Create game record
        game = Game.objects.create(
            user=request.user,
            difficulty=difficulty,
            result=result,
            time_taken=time_taken,
            attempts_used=attempts_used,
            max_attempts=config['attempts']
        )
        
        # Update statistics
        if hasattr(request.user, 'statistics'):
            request.user.statistics.update_statistics()
        
        return JsonResponse({
            'success': True,
            'message': 'Game result saved successfully.',
            'game_id': game.id
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error saving game result: {str(e)}'
        }, status=400)


@login_required
def profile_view(request):
    """User profile view with statistics"""
    profile = request.user.profile
    stats = profile.get_statistics()
    recent_games = Game.objects.filter(user=request.user)[:10]
    
    context = {
        'stats': stats,
        'recent_games': recent_games
    }
    
    return render(request, 'memory_game/profile.html', context)


@login_required
def game_history_view(request):
    """Complete game history view"""
    games = Game.objects.filter(user=request.user)
    
    context = {
        'games': games
    }
    
    return render(request, 'memory_game/game_history.html', context)
