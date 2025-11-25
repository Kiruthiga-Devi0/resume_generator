from rest_framework import serializers

class FileScoreRequestSerializer(serializers.Serializer):
    resume_file = serializers.FileField()
    job_description = serializers.CharField()
