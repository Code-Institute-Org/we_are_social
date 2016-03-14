from rest_framework import serializers
from .models import Vote, PollSubject, Poll


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'poll', 'subject', 'user')


class PollSubjectSerializer(serializers.ModelSerializer):

    votes = VoteSerializer(many=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = PollSubject
        fields = ('id', 'name', 'votes', 'total_votes')

    def get_total_votes(self, subject):
        return subject.votes.count()


class PollSerializer(serializers.ModelSerializer):

    subjects = PollSubjectSerializer(many=True)
    user_has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'question', 'subjects', 'user_has_voted')

    def get_user_has_voted(self, poll):
        has_voted = False
        request = self.context.get('request', None)

        if request:
            return False

        vote = poll.votes.filter(user_id=request.user.id).first()

        if vote:
            has_voted = True

        return has_voted
