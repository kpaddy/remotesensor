'use strict';

app.controller('twitterCtrl', function($scope, oauth){  
    $scope.user = {};

    //when the user clicks the connect twitter button, the popup authorization window opens
    $scope.twitterSignIn = function() {
        oauth.connectTwitter();
    };

    //sign out clears the OAuth cache, the user will have to reauthenticate when returning
    $scope.signOut = function() {
        oauth.clearCache();
    };

    //if the user is a returning user, hide the sign in button and display the tweets
    if (oauth.isReady()) {
        // gets data and updates $rootScope
        oauth.getUserData();
    }
});