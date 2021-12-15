from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class SubLinkList(models.Model):
    url = fields.TextField()
    sublinks = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


SubLinkListSchema = pydantic_model_creator(SubLinkList)
