from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import (
    viewsets,
    mixins,
    status,
    views,
    response,
    generics,
)


from . import serializers, models, filters, services
from .authentication import expiring_token_authentication
from horeca_utils import utils
from candidate_tests import selectors as tests_selectors
from candidate_tests.serializers import TestingSessionSerializer


class AdminViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin):

    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminSerializer


class ManagerViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin):

    queryset = models.Manager.objects.all()
    serializer_class = serializers.ManagerSerializer


class CondidateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CandidateSerializer
    pagination_class = utils.StandardResultsSetPagination
    filterset_class = filters.CandidateFilter

    @action(methods=['delete'], detail=False, url_path='bulk-delete')
    def bulk_destroy(self, request):
        serializer = serializers.CandidateBulkDestroySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        models.User.objects.filter(candidate__pk__in=serializer.data['candidates']).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='get-test-result')
    def get_test_result(self, request, pk=None):
        candidate = self.get_object()
        data = tests_selectors.get_tests_results(candidate)
        return response.Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='get-test-result')  # TODO: Переписать это дерьмо
    def get_tests_results(self, request, pk=None):
        candidates = request.data['candidates']
        data = self._get_candidates_tests_results(candidates)
        return response.Response(data=data, status=status.HTTP_200_OK)

    def _get_candidates_tests_results(self, candidates):  # И это
        candidates = models.Candidate.objects.filter(pk__in=candidates).all()
        candidate_serializer = serializers.CandidateSerializer(data=candidates, many=True)
        candidate_serializer.is_valid()
        return candidate_serializer.data

    def destroy(self, request, pk=None):
        models.User.objects.get(candidate__pk=pk).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user.related_object
        queryset = None

        if isinstance(user, models.Admin):
            queryset = models.Candidate.objects.all().order_by('-user__date_joined')
        elif isinstance(user, models.Manager):
            queryset = user.candidatecreator.candidates.all().order_by('-user__date_joined')

        return queryset

    @action(methods=['post'], detail=False, url_path='create-testing-session')
    def create_testing_session(self, request):
        serializer = TestingSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = {'testing_status': instance.candidate.testing_status}
        return response.Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='filter')
    def filter_candidate(self, request):
        paginator = self.pagination_class()
        serializer = serializers.CandidateFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.get_queryset()
        filterset = filters.CandidateFilter(data=serializer.data)
        filterset.is_valid()
        queryset = filterset.filter_queryset(queryset=queryset)

        paginated_queryset = paginator.paginate_queryset(queryset, request)
        data = self.serializer_class(paginated_queryset, many=True).data
        r = paginator.get_paginated_response(data)
        return r

    @action(methods=['post'], detail=False, url_path='download-pdf')
    def download_pdf(self, request):
        serializer = serializers.DownloadPdfSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate = serializer.data['candidate']
        link = services.get_pdf_download_links(candidate)
        return response.Response(data=link, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='positions', permission_classes=[AllowAny])
    def get_positions(self, request):
        data = models.Position.objects.all().values_list('title', flat=True)
        return response.Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='comment')
    def write_comment(self, request):
        serializer = serializers.CandidateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate = self.get_queryset().get(pk=serializer.data['candidate'])
        candidate.comment = serializer.data['text']
        candidate.save(update_fields=['comment'])
        response_data = self.serializer_class(candidate).data
        return response.Response(data=response_data, status=status.HTTP_200_OK)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        # Создать новый токен, если время жизни текущего истекло
        is_expired, token = expiring_token_authentication.token_expire_handler(token)

        return response.Response({
            'token': token.key,
            'user_id': user.pk,
            'user_type': user.related_object.__class__.__name__,
        })


class Logout(views.APIView):
    def post(self, request, format=None):
        request.user.token.delete()
        return response.Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = serializers.ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.data.get("new_password"))
        user.save(update_fields=['password'])

        return response.Response(data={'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


class GetMeView(generics.RetrieveAPIView):
    def get_object(self):
        return self.request.user.related_object

    def get_serializer_class(self):
        user = self.get_object()
        serializer_class = None

        if isinstance(user, models.Admin):
            serializer_class = serializers.AdminSerializer
        elif isinstance(user, models.Manager):
            serializer_class = serializers.ManagerSerializer
        elif isinstance(user, models.Candidate):
            serializer_class = serializers.CandidateSerializer

        return serializer_class

    def get(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if serializer_class is None:
            return response.Response(data={'message': 'User is not found'}, status=status.HTTP_400_BAD_REQUEST)
        return self.retrieve(request, *args, **kwargs)
