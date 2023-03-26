from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FollowRequest, Profile
from .serializers import FollowRequestSerializer

User = get_user_model()


class ProfileDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):

    model = Profile
    success_message = _("Sucess message in profile")

    def get_object(self):
        if "username" in self.kwargs:
            return User.objects.get(username=self.kwargs["username"]).profile
        else:
            return self.request.user.profile


profile_detail_view = ProfileDetailView.as_view()


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Profile
    fields = [
        "artist_name",
        "location",
        "bio",
    ]
    success_message = _("Information successfully updated")

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return reverse("artists:detail")


profile_update_view = ProfileUpdateView.as_view()


class MyReceivedFollowRequestList(APIView):
    def get(self, request, format=None):
        follow_requests = FollowRequest.objects.filter(to_profile=request.user.profile)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return Response(serializer.data)


class MySentFollowRequestList(APIView):
    def get(self, request, format=None):
        follow_requests = FollowRequest.objects.filter(
            from_profile=request.user.profile
        )
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """{"from_profile":1, "to_profile":1}"""
        request.data["status"] = FollowRequest.CREATED
        request.data["from_profile"] = request.user.profile.pk
        serializer = FollowRequestSerializer(data=request.data)
        if serializer.is_valid():
            if (
                serializer.validated_data["to_profile"]
                == serializer.validated_data["from_profile"]
            ):
                return Response(
                    "Impossible to make a follow request to oneself",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            follow_request = FollowRequest.objects.get(
                from_profile=request.user.profile, to_profile=request.data["to_profile"]
            )
            follow_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FollowRequest.DoesNotExist:
            raise Http404
        except KeyError:
            return Response(
                "You must provide a to_profile field",
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowRequestDetail(APIView):
    def get_object(self, pk):
        try:
            return FollowRequest.objects.get(pk=pk)
        except FollowRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        follow_request = self.get_object(pk)
        if request.user.profile in (
            follow_request.from_profile,
            follow_request.to_profile,
        ):
            serializer = FollowRequestSerializer(follow_request)
            return Response(serializer.data)
        raise Http404

    def put(self, request, pk, format=None):
        follow_request = self.get_object(pk)
        if request.user.profile == follow_request.to_profile:
            try:
                if request.data["status"] == str(FollowRequest.ACCEPTED):
                    follow_request.accept()
                elif request.data["status"] == str(FollowRequest.REJECTED):
                    follow_request.reject()
                else:
                    Response(
                        "You are not allowed to set the follow request status to {}".format(
                            request.data["status"]
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                serializer = FollowRequestSerializer(follow_request)
                return Response(serializer.data)
            except KeyError:
                return Response(
                    "You must provide a status field",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            "You are not allowed to modify the follow request if you are not its target",
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        follow_request = self.get_object(pk)
        if request.user.profile == follow_request.from_profile:
            follow_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            "You are not allowed to delete a follow request if you are not the creator",
            status=status.HTTP_400_BAD_REQUEST,
        )
