from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile



@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('user is updated')
        except:
            # create the userprofile if does not exist
            UserProfile.objects.create(user=instance)
            print('user profile does not exist. So created a new one')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')
# post_save.connect(post_save_create_profile_receiver)