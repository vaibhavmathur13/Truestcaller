from django.db.models import Q, Case, When, Value, Count, F

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from truestcaller import (
    serializers as truestcaller_serializers,
    models as truestcaller_models,
    utils as truestcaller_utils
)


class RegisterUserAPIView(generics.CreateAPIView):
    """
    This API registers a user in the app.
    It takes user's name, phone number, password.
    Email is optional.
    After registering, a user is given it's unique
    Token.
    """
    serializer_class = truestcaller_serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super(RegisterUserAPIView, self).post(request, *args, **kwargs)
        user = truestcaller_models.User.objects.get(phone_number=response.data['phone_number'])
        token = Token.objects.create(user=user)
        response.data['token'] = token.key
        return response


class LoginUserAPIView(ObtainAuthToken):
    """
    Endpoint of Login API to let users login.
    Token generated in Register API is validated here
    and then only a user can login.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Give token along with user_id and password to user that provides valid credentials
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'phone_number': user.phone_number
        })


class PhoneNumberSpamMarkAPIView(generics.UpdateAPIView):
    """
    After logging in, this API let users' update the Directory
    model's is_span attribute. A user can mark/unmark a number
    as spam.
    """
    serializer_class = truestcaller_serializers.PhoneNumberSpamSerializer

    authentication_classes = [TokenAuthentication]

    def get_object(self):
        if not self.request.data.get('phone_number'):
            raise ValidationError('Please provide a valid phone number first.')

        if self.request.data.get('phone_number') == self.request.user.phone_number:
            raise ValidationError('You cannot mark/unmark yourself spam')

        instance, created = truestcaller_models.Directory.objects.get_or_create(
            added_by=self.request.user, phone_number=self.request.data['phone_number']
        )
        return instance


class SearchByNameAPIView(generics.ListAPIView):
    """
    This API, when provided a name, returns a list of
    all names where the instance of the provided name
    is present.
    This list is in order in which it should be according
    to the Project description.
    """
    serializer_class = truestcaller_serializers.CustomSearchSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        name = self.request.data.get('name', "")
        phone_number_list_for_people_email = truestcaller_utils.get_people_for_email(self.request.user.phone_number)
        query_set = truestcaller_models.Directory.objects.filter(
            Q(name__startswith=name) | Q(name__contains=name)
        ).annotate(
            is_start_with=Case(
                When(name__startswith=name, then=Value(True)),
                default=Value(False)
            ),
            email=Case(
                When(Q(phone_number__in=phone_number_list_for_people_email),
                     then='added_by__email'),
                default=Value(None)
            )
        ).order_by('-is_start_with')
        return query_set


class SearchByPhoneNumberAPIView(generics.ListAPIView):
    """
    When search is done through phone number, if the
    number is registered, the API will show the result
    from the registered users' table. If not registered,
    a list will return of all records.
    """
    serializer_class = truestcaller_serializers.CustomSearchSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if not self.request.data.get('phone_number'):
            raise ValidationError("Enter a Phone Number to search")

        phone_number_list_for_people_email = truestcaller_utils.get_people_for_email(self.request.user.phone_number)
        phone_number = self.request.data['phone_number']
        query_set = truestcaller_models.Directory.objects.filter(
            added_by__phone_number=phone_number, phone_number=phone_number
        ).annotate(
            email=Case(
                When(Q(phone_number__in=phone_number_list_for_people_email),
                     then='added_by__email'),
                default=Value(None)
            )
        )

        if not query_set.exists():
            query_set = truestcaller_models.Directory.objects.filter(
                phone_number=phone_number
            )

        return query_set

    def get(self, request, *args, **kwargs):
        response = super(SearchByPhoneNumberAPIView, self).get(request, *args, **kwargs)
        spam_likelihood = truestcaller_models.Directory.objects.filter(
            phone_number=request.data.get('phone_number'), is_spam=True
        ).count()
        user_list = response.data
        response.data = {'user_list': user_list, 'spam_likelihood': spam_likelihood}
        return response


class LogoutAPIView(APIView):
    """
    This API simply deletes the token of a logged in user.
    This can happen either by clicking logout or the session
    times out.
    """
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
