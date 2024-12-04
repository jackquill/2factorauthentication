from django.db import models
from users.models  import CustomUser
import secrets
import string

class Code(models.Model):
    number = models.CharField(max_length= 5, blank=True) #code will be 5 charcters long can be initailly blank
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) #link code model to customUser model

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
       # print("Save method called")  # debugging

        code_length = 5
        #secrets is used to create secure codes in this case it will create a 5 digit code
        secure_code = ''.join(secrets.choice(string.digits) for i in range(code_length))

        self.number = secure_code  # assign  generated code to the number field
        super().save(*args, **kwargs)  # call the parent save method


    