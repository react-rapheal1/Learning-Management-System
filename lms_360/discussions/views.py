from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .models import Discussion
from .serializers import DiscussionSerializer, DiscussionReplySerializer, DiscussionCreateSerializer
from . services import (
    get_discussion,
    toggle_like,
    toggle_follow,
    add_view,
    create_reply
)

from core.permissions import IsEnrolledInDiscussion


class DiscussionListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Discussions'],
        summary="List discussions",
        description="Retrieve a list of discussions with optional filtering by tab (my, following, unanswered), search, and sorting.",
        parameters=[
            {
                "name": "tab",
                "in": "query",
                "description": "Filter discussions by tab: 'my' (user's discussions), 'following' (followed discussions), 'unanswered' (discussions with no replies)",
                "schema": {"type": "string", "enum": ["my", "following", "unanswered"]}
            },
            {
                "name": "search",
                "in": "query",
                "description": "Search discussions by title or content",
                "schema": {"type": "string"}
            },
            {
                "name": "sort",
                "in": "query",
                "description": "Sort discussions by: 'likes', 'replies', 'views', or default (newest first)",
                "schema": {"type": "string", "enum": ["likes", "replies", "views"]}
            }
        ],
        responses={
            200: DiscussionSerializer(many=True),
        }
    )
    def get(self, request):
        tab = request.GET.get('tab')
        search = request.GET.get('search')
        sort = request.GET.get('sort')

        discussions = get_discussion(
            user = request.user,
            tab = tab,
            search=search,
            sort=sort
        )

        serializer = DiscussionSerializer(discussions, many = True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Discussions'],
        summary="Create discussion",
        description="Create a new discussion. User must be enrolled in the specified course.",
        request=DiscussionCreateSerializer,
        responses={
            201: DiscussionSerializer,
            400: "Bad request - invalid data",
            403: "Forbidden - not enrolled in course"
        }
    )
    def post(self, request):
        serializer = DiscussionCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if user is enrolled in the course
            course = serializer.validated_data['course']
            if not course.enrollments.filter(user=request.user).exists():
                return Response({"error": "You must be enrolled in the course to create discussions"}, status=403)

            serializer.save(author=request.user)
            # Return the full discussion with counts
            discussion = Discussion.objects.filter(id=serializer.instance.id).annotate(
                likes_count=0,  # New discussion has no likes yet
                replies_count=0,
                views_count=0,
            ).first()
            response_serializer = DiscussionSerializer(discussion)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DiscussionLikeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Like/unlike discussion",
        description="Toggle like status for a discussion. Returns whether the discussion is now liked.",
        responses={
            200: {"liked": True},
            404: "Discussion not found"
        }
    )
    def post(self, request, pk):
        discussion = get_object_or_404(Discussion, pk = pk)
        liked = toggle_like(discussion, request.user)

        return Response({"liked": liked})
    

class DiscussionFollowView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Follow/unfollow discussion",
        description="Toggle follow status for a discussion. Returns whether the discussion is now followed.",
        responses={
            200: {"followed": True},
            404: "Discussion not found"
        }
    )
    def post(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)
        followed = toggle_follow(discussion, request.user)

        return Response({"followed": followed})

class DiscussionReplyView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Reply to discussion",
        description="Create a reply to a discussion.",
        request={
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Reply content"}
            },
            "required": ["content"]
        },
        responses={
            200: DiscussionReplySerializer,
            404: "Discussion not found"
        }
    )
    def post(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)
        content = request.data.get("content")

        reply = create_reply(discussion, request.user, content)
        serializer = DiscussionReplySerializer(reply)

        return Response(serializer.data)
    

class DiscussionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsEnrolledInDiscussion]

    @extend_schema(
        summary="Get discussion details",
        description="Retrieve detailed information about a specific discussion. User must be enrolled in the course.",
        responses={
            200: DiscussionSerializer,
            403: "Forbidden - not enrolled in course",
            404: "Discussion not found"
        }
    )
    def get(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)

        add_view(discussion, request.user)

        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data)




