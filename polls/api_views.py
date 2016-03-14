from rest_framework import generics, status
from rest_framework.response import Response
from models import Poll, Vote, PollSubject
from serializers import PollSerializer, VoteSerializer
from threads.models import Thread


class PollViewSet(generics.ListAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollInstanceView(generics.RetrieveAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class VoteCreateView(generics.ListCreateAPIView):

    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def create(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        subject = thread.poll.votes.filter(user=request.user).first()

        if subject:
            return Response({"error": "Already voted!"},
                            status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = request.user.id
        serializer = VoteSerializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            thread.poll.votes.add(serializer.instance)

            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
