from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user')
    user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE, related_name='userprofile')
    vendor_name = models.CharField(max_length=100)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        # check if the vendor is already created, 
        # with this conditions it means that the table is already created
        # and now its updating.
        if self.pk is not None:
            
            # orig = original status of the approved checkbox
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user' : self.user,
                    'is_approved' : self.is_approved,
                }

                if self.is_approved == True:
                    # Send the notification email
                    mail_subject = 'Congatulation. Your restuarant has been approved'
                    send_notification(mail_subject, mail_template, context)

                else:
                    # Send the notification email
                    mail_subject = 'We are sorry. You are not eligible for publishing your food menu on our marketplace'
                    send_notification(mail_subject, mail_template, context)


        return super(Vendor, self).save(*args, **kwargs)