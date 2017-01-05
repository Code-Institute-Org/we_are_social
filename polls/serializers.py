from rest_framework import serializers
from .models import Vote, PollSubject, Poll


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('id', 'poll', 'subject', 'user')


class PollSubjectSerializer(serializers.ModelSerializer):

    votes = VoteSerializer(many=True)
    percentage_of_votes = serializers.SerializerMethodField()

    class Meta:
        model = PollSubject
        fields = ('id', 'name', 'votes', 'percentage_of_votes')

    def get_percentage_of_votes(self, subject):
        try:
            return subject.votes.count() / subject.poll.votes.count() * 100
        except ZeroDivisionError:
            # Return a percentage of 0 when there were no votes yet
            return 0


class PollSerializer(serializers.ModelSerializer):

    subjects = PollSubjectSerializer(many=True)
    user_has_voted = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ('id', 'question', 'subjects',
                  'user_has_voted', 'total_votes')

    def get_user_has_voted(self, poll):
        has_voted = False
        request = self.context.get('request', None)

        if request:
            return False

        if not request.user.is_authenticated():
            return True

        vote = poll.votes.filter(user_id=request.user.id).first()

        if vote:
            has_voted = True

        return has_voted

    def get_total_votes(self, poll):
        return poll.votes.count()
