from rest_framework import serializers

from product.models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'start_date', 'cost', 'author', 'min_students', 'max_students', 'num_lessons']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']
