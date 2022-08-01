
# I'm trying to create a function that automatically delete an object after 5 minutes from publication.

# from django.contrib.gis.db import models
# from django.utils import timezone

# import datetime

# class Event(models.Model):
#     name = models.CharField(
#         max_length=100,
#         )
#     publishing_date = models.DateTimeField(
#     default=timezone.now,
#     blank=True,
#     )

#     @property
#     def delete_after_five_minutes(self):
#         time = self.publishing_date + datetime.timedelta(minutes=5)
#         if time > datetime.datetime.now():
#             e = Event.objects.get(pk=self.pk)
#             e.delete()
#             return True
#         else:
#             return False
# The problem is that all objects are deleted and not only the objects that I wish.

# python-3.x
# django-models
# django-2.2
# Share
# Follow
# asked Jul 30, 2019 at 8:55
# user avatar
# Massimiliano Moraca
# 8931111 silver badges2727 bronze badges
# 1
# You should swap to comparison, so time < datetime.datetime.now(). – 
# Willem Van Onsem
#  Jul 30, 2019 at 8:57
# Add a comment
# 1 Answer
# Sorted by:

# Highest score (default)

# 2

# You should swap the comparison, so:

# if time < datetime.datetime.now():
#     # ...
# or perhaps more readable:

# if self.publishing_date < datetime.datetime.now()-datetime.timedelta(minutes=5):
#     # ...
# since this thus means that five minutes before now is still after the time when the Event was published.

# That being said, it might be better not to delete the values, or at least not immediately, but make a manager, that simply "hides" these objects. You can then later, periodically, remove the elements.

# We can make such manager with:

# from django.utils import timezone

# class EventManager(models.Manager):

#     def get_queryset(self):
#         return super().get_queryset().filter(
#             publishing_date__gte=timezone.now()-timezone.timedelta(minutes=5)
#         )
# and then use this manager like:

# class Event(models.Model):
#     # ...
#     objects = EventManager()
# Then Event.objects will only retrieve Events that have been published less than five minutes ago.

# You can periodically remove such events with:

# Event._base_manager.filter(
#     publishing_date__lt=timezone.now()-timezone.timedelta(minutes=5)
# ).delete()
# This will then remove these Events in "bulk".

# Share
# Follow
# answered Jul 30, 2019 at 9:02
# user avatar
# Willem Van Onsem
# 406k2929 gold badges377377 silver badges495495 bronze badges
# 1
# Oh great, it's run! I had no idea that is possible "to put in standby" an object using something like EventManager. I must improve my skills with Python and Django. Thank you :) – 
# Massimiliano Moraca
#  Jul 30, 2019 at 9:28
# 1
# @MassimilianoMoraca: there is also a django-softdelete package that might/might not help: github.com/scoursen/django-softdelete – 
# Willem Van Onsem
#  Jul 30, 2019 at 9:29
# Note that filtering the base queryset in the default manager is to be done with caution, cf docs.djangoproject.com/en/2.2/topics/db/managers/…. – 
# bruno desthuilliers
#  Jul 30, 2019 at 11:47
# @brunodesthuilliers: I agree. Probably it is better to use a package like softdelete since then one can use names like .active_objects and .all_objects for the managers. – 
# Willem Van Onsem
#  Jul 30, 2019 at 11:51