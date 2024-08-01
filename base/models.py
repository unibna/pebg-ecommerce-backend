from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    @classmethod
    def is_field_validated(cls, field):
        field = field.lower().\
                    strip(" ").\
                    rstrip(" ").\
                    replace(" ", "_").\
                    replace("-", "_")
        return hasattr(cls, field)
