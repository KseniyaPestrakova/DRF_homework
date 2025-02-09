from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import UrlValidator
from users.models import Subscribe


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    count_lessons_in_course = serializers.SerializerMethodField()
    is_subscribe = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribe(self, course):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, course=course).exists()
        return False

    class Meta:
        model = Course
        fields = ("name", "description", "count_lessons_in_course", "is_subscribe", "lessons")
