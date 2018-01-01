from django.contrib.auth.models import User
from django.db import models, router
from django.core.exceptions import ValidationError
from django.db.models.deletion import Collector
from django.core.files.storage import default_storage

from dbg.settings import DEBUG
from PIL import Image


class BaseModel(models.Model):
    """
        Parent model
        :model:`djangoplaza.BaseModel`
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def can_delete(self):
        """
            Selects which fields of the base model can be deleted
        """
        if self._get_pk_val():
            seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
            seen_objs.collect([self])
            if len(seen_objs.data) > 1:
                raise ValidationError("Sorry, cannot be deleted. {}".format(seen_objs.data))

    def can_delete_special(self):
        """
            Selects which fields of the base model can be deleted
        """
        if self._get_pk_val():
            seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
            seen_objs.collect([self])
            if len(seen_objs.data) > 2:
                raise ValidationError("Sorry, cannot be deleted. {}".format(seen_objs.data))

    def delete(self, **kwargs):
        """
            Deletes fields from base model
        """
        assert self._get_pk_val() is not None, "Object %s cannot be deleted because %s is null." % (
            self._meta.object_name, self._meta.pk.attname)
        seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
        seen_objs.collect([self])
        self.can_delete()
        seen_objs.delete()

    def delete_special(self, **kwargs):
        """
            Deletes fields from base model
        """
        assert self._get_pk_val() is not None, "Object %s cannot be deleted because %s is null." % (
            self._meta.object_name, self._meta.pk.attname)
        seen_objs = Collector(router.db_for_write(self.__class__, instance=self))
        seen_objs.collect([self])
        self.can_delete_special()
        seen_objs.delete()

    # def resize_image(self, image_field, width=640, height=480):
    #
    #     # If the image was modified, Django stores it temporarily inside the wrapper InMemoryUploadedFile before
    #     # storing it inside the hard drive. Only in that case we want to modify the image, otherwise the image has not
    #     # been updated by the user and no processing should be done on it
    #     if not DEBUG:
    #         if image_field:
    #             # Open the uploaded image
    #             with default_storage.open(image_field.path, 'rb') as current_file:
    #
    #                 im = Image.open(current_file)
    #
    #                 # Transform all the images to JPG format to apply optimizations
    #                 im = im.convert('RGB')
    #
    #                 # Resize the image
    #                 # If the size of the image is smaller than the required, don't resize
    #                 if im.size > (width, height):
    #                     wpercent = (width / float(im.size[0]))
    #                     new_height = int((float(im.size[1]) * float(wpercent)))
    #
    #                     im = im.resize((width, new_height), Image.ANTIALIAS)
    #
    #                 # After modifications, save it to the path
    #                 im.save(image_field.path, format='JPEG', quality=90, optimize=True)

    def save(self, **kwargs):
        # If the model contains an image, avatar or icon, transform it into a 640 x 480 px before saving the model
        fields = [field.name for field in self._meta.get_fields()]
        # if 'image' in fields and self.image:
        #     if os.path.isfile(self.image.path):
        #         self.resize_image(self.image)
        # if 'avatar' in fields and self.avatar:
        #     if os.path.isfile(self.avatar.path):
        #         self.resize_image(self.avatar)
        # if 'icon' in fields and self.icon:
        #     if os.path.isfile(self.icon.path):
        #         self.resize_image(self.icon)
        # if 'cover' in fields and self.cover:
        #     if os.path.isfile(self.cover.path):
        #         self.resize_image(self.cover)

        models.Model.save(self)

    class Meta:
        abstract = True


class UsersGroup(BaseModel):
    name = models.CharField(max_length=100)
    # This is the plan a premium user account subscribes to for a user group

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Users Group'
        verbose_name_plural = 'Users Group'
        db_table = 'users_group'
        unique_together = ('name',)


class Users(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    user = models.OneToOneField(User)
    group = models.ForeignKey(UsersGroup, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.FileField(upload_to='images/', max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        unique_together = ('user',)


class Clients(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        db_table = 'clients'


class ClientsUsers(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    client = models.OneToOneField(Clients)
    user = models.OneToOneField(Users)

    def __str__(self):
        return "{} - {}".format(self.client, self.user)

    class Meta:
        verbose_name = 'Client User'
        verbose_name_plural = 'Clients Users'
        db_table = 'clients_users'
        unique_together = ('client', 'user')


class Domains(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    client = models.OneToOneField(Clients)
    name = models.CharField(max_length=20, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    year_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    month_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'
        db_table = 'domains'


class Hosting(BaseModel):
    """
        Model used to define a user according to the following fields:
    """
    client = models.OneToOneField(Clients)
    domain = models.OneToOneField(Domains)
    name = models.CharField(max_length=20, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    year_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    month_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Hosting'
        verbose_name_plural = 'Hostings'
        db_table = 'hostings'

