# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, max_length=100)
    content = serializers.CharField(required=False, max_length=500)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=5)
    dueDate = serializers.DateTimeField(required=False)
    isFulfilled = serializers.BooleanField(required=False)

    def create(self, validated_data):
        if(validated_data.get('title') == None or validated_data.get('content') == None):
            raise Exception("both title and content are required.")
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.dueDate = validated_data.get('dueDate', instance.dueDate)
        instance.isFulfilled = validated_data.get('isFulfilled', instance.isFulfilled)
        instance.save()
        return instance
