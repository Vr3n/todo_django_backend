from rest_framework import serializers
import datetime

from .models import Todo

# Create your serializers here.


class TodoSerializer(serializers.ModelSerializer):

    start_date = serializers.DateField(initial=datetime.date.today)

    class Meta:
        model = Todo
        fields = ['title',
                  'description',
                  'is_completed',
                  'start_date',
                  'end_date']
