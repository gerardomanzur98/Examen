from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count


class UserProfile(models.Model):
    """Extended user profile to store additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_statistics(self):
        """Calculate and return user statistics"""
        games = Game.objects.filter(user=self.user)
        total_games = games.count()
        total_wins = games.filter(result='win').count()
        total_losses = games.filter(result='loss').count()
        
        # Calculate average time for completed games
        avg_time = games.filter(result='win').aggregate(Avg('time_taken'))['time_taken__avg']
        avg_time = round(avg_time, 2) if avg_time else 0
        
        # Find most played level
        most_played = games.values('difficulty').annotate(
            count=Count('difficulty')
        ).order_by('-count').first()
        most_played_level = most_played['difficulty'] if most_played else 'N/A'
        
        return {
            'total_games': total_games,
            'total_wins': total_wins,
            'total_losses': total_losses,
            'average_time': avg_time,
            'most_played_level': most_played_level,
            'win_rate': round((total_wins / total_games * 100), 2) if total_games > 0 else 0
        }


class Game(models.Model):
    """Model to store individual game records"""
    DIFFICULTY_CHOICES = [
        ('basic', 'Basic - 6 attempts'),
        ('medium', 'Medium - 4 attempts'),
        ('advanced', 'Advanced - 2 attempts'),
    ]
    
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('loss', 'Loss'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    time_taken = models.FloatField(help_text="Time taken in seconds")
    attempts_used = models.IntegerField(help_text="Number of failed attempts")
    max_attempts = models.IntegerField(help_text="Maximum attempts allowed")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.difficulty} - {self.result} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @staticmethod
    def get_difficulty_config(difficulty):
        """Return configuration for each difficulty level"""
        configs = {
            'basic': {'attempts': 6, 'time_limit': 60},
            'medium': {'attempts': 4, 'time_limit': 60},
            'advanced': {'attempts': 2, 'time_limit': 60},
        }
        return configs.get(difficulty, configs['basic'])


class GameStatistics(models.Model):
    """Aggregate statistics per user (optional, for caching)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    total_games = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    total_losses = models.IntegerField(default=0)
    average_time = models.FloatField(default=0.0)
    most_played_level = models.CharField(max_length=10, default='basic')
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Game Statistics"
    
    def __str__(self):
        return f"Statistics for {self.user.username}"
    
    def update_statistics(self):
        """Update statistics based on game records"""
        profile = self.user.profile
        stats = profile.get_statistics()
        
        self.total_games = stats['total_games']
        self.total_wins = stats['total_wins']
        self.total_losses = stats['total_losses']
        self.average_time = stats['average_time']
        self.most_played_level = stats['most_played_level']
        self.save()
