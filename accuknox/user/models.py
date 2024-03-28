from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .choices import STATUS_CHOICES

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,  email, name, password=None):
        
        email = self.normalize_email(email) # for case insensitive email

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, name=None):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model( email=email, name=name)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=254, default=None)
    password = models.CharField(max_length=254, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"  # Show same Name in Admin Panel


class Friendship(models.Model):
   
    sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.status}"