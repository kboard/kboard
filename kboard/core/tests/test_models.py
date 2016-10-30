from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.db import models
from django.test import TestCase

from core.models import TimeStampedModel


class TestModelInheritedTimeStampedModel(TimeStampedModel):
    name = models.TextField(default='')

    class Meta:
        app_label = 'core'


class TestTimeStampedModel(TestCase):
    def test_created_time_after_create_Inherited_TimeStampedModel(self):
        test_model = TestModelInheritedTimeStampedModel()
        test_model.save()

        time_after_create = datetime.now(timezone.utc)

        self.assertGreater(timedelta(minutes=1), time_after_create - test_model.created_time)

    def test_modified_time_after_modify_Inherited_TimeStampedModel(self):
        test_model = TestModelInheritedTimeStampedModel()
        test_model.save()

        test_model.name = "modified name"
        test_model.save()

        time_after_modify = datetime.now(timezone.utc)

        self.assertGreater(timedelta(minutes=1), time_after_modify - test_model.modified_time)
