from rest_framework import serializers

from . import models


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Table
        fields = ('name', 'data')




