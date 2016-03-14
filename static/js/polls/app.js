/**
 * Created by Aaron on 14/03/2016.
 */

var pollApp = angular.module('pollApp', []);

pollApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
});

pollApp.factory('pollFactory', function($http) {
    var pollUrl = '/threads/polls/';
    var votingUrl = '/threads/polls/vote/';

    pollFactory = {};

    pollFactory.getPoll = function(id) {
        return $http.get(pollUrl + id);
    };

    pollFactory.vote = function(poll, subject) {
        var data = {'poll': poll.id, 'subject': subject.id};

        return $http.post(votingUrl + poll.thread + '/', data);
    };

    return pollFactory;
});

pollApp.controller('PollCtrl', function($scope, pollFactory) {
    $scope.poll = "";

    function setPoll(response) {
        $scope.poll = response.data;
        console.log($scope.poll)
    }

    function showError(response) {
        if (response.data.error !== undefined) {
            alert(response.data.error)
        }
    }

    function getPoll() {
        console.log($scope.poll.id);
        console.log(pollFactory.getPoll(1))
        return pollFactory.getPoll(pollID);
    }

    getPoll().then(setPoll);

    $scope.vote = function(poll, subject) {
        pollFactory.vote(poll, subject).then(getPoll).then(setPoll, showError);
    }
});