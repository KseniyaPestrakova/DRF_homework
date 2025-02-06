from rest_framework import serializers
from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'count_lessons_in_course', 'lessons')






