from django.db import models
from common.models import CommonModel
from django.core.validators import MinLengthValidator

# Create your models here.


class Chat(CommonModel):
    content = models.CharField(max_length=2000, validators=[MinLengthValidator(1)])
    writer = models.ForeignKey(
        "users.User",
        related_name="chats",
        on_delete=models.CASCADE,
    )
