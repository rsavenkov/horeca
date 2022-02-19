from rest_framework import serializers

from . import models, validators, selectors
from horeca_utils import constants
from candidate_tests.selectors import get_tests_results


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        validators = [validators.UniqueEmailValidator()]

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        request = self.context.get('request', None)

        # TODO: AHC-241 выглядит как костыль - переписать
        if request and 'get-me' in request.path:
            ret['user_type'] = obj.__class__.__name__

        return ret


class AdminSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = models.Admin
        fields = '__all__'


class ManagerSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = models.Manager
        fields = '__all__'

    # Нужно для обработки пустой строки при создании менджера (Key (taxpayer_id_number)=() already exists)
    def save(self, **kwargs):
        if self.validated_data.get('taxpayer_id_number', None) == '':
            self.validated_data['taxpayer_id_number'] = None
        return super().save(**kwargs)

    def to_representation(self, obj):
        ret = super().to_representation(obj)

        if ret['taxpayer_id_number'] is None:
            ret['taxpayer_id_number'] = ''

        return ret


class CandidateFilterSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    testing_status = serializers.MultipleChoiceField(choices=constants.TESTING_STATUSES, required=False)
    from_date_joined = serializers.DateField(required=False)
    to_date_joined = serializers.DateField(required=False)
    company = serializers.CharField(required=False)


class CandidateCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CandidateCreator
        fields = ['admin', 'manager']

    admin = AdminSerializer(read_only=True)
    manager = ManagerSerializer(read_only=True)


class DownloadPdfSerializer(serializers.Serializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=models.Candidate.objects.all())


class CandidateCommentSerializer(serializers.Serializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=models.Candidate.objects.all())
    text = serializers.CharField(allow_blank=True)


class CandidateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = models.Candidate
        fields = '__all__'

    tests_results = serializers.SerializerMethodField()
    # testing_status = serializers.SerializerMethodField()

    def get_tests_results(self, obj):
        data = get_tests_results(obj)
        try:
            data = get_tests_results(obj)
        except AttributeError:
            data = None

        return data

    # def get_testing_status(self, obj):
    #     return selectors.get_candidate_testing_status(obj)

    def to_internal_value(self, data):
        user = self.context['request'].user.related_object
        creator = selectors.get_candidate_creator(user)
        data['creator'] = creator.pk
        return super().to_internal_value(data)

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        ret['creator'] = CandidateCreatorSerializer(obj.creator).data
        ret['date_joined'] = obj.user.date_joined.__str__()
        return ret


class CandidateBulkDestroySerializer(serializers.Serializer):
    candidates = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Candidate.objects.all())


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        return attrs
