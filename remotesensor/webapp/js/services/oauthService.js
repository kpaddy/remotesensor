app.service('oauth', function(OAUTH_PUBLIC_KEY, $q, $http, $window, $rootScope){  
    var authorizationResult = false;

    return {
        initialize: function() {
            $rootScope.currentUser = false;

            //initialize OAuth.io with public key of the application
            OAuth.initialize(OAUTH_PUBLIC_KEY, {
                cache: true
            });
            //try to create an authorization result when the page loads,
            // this means a returning user won't have to click the twitter button again
            authorizationResult = OAuth.create("twitter");
        },
        isReady: function() {
            return (authorizationResult);
        },
        connectTwitter: function() {
            var deferred = $q.defer();
            var self = this;

            OAuth.popup("twitter", {
                cache: true
            }, function(error, result) {
                if (!error) {
                    // update token
                    authorizationResult = result;

                    // get data from twitter
                    self.getUserData();
                    deferred.resolve();

                } else {
                    // shit shit fire ze missiles
                    deferred.reject();
                    $window.location.href = '/remotesensor/app/#/sensors';
                    // {
                    //    "oauth_token": "3354456526-6Nv5MDrhgwwKyVqgwFc15RYqJ4sj6FmAyx2z0R3",
                    //    "oauth_token_secret": "OzSWDM24Rippx8BNIMozQUSAkiFmbttWRIK1kjOejh5jF",
                    //    "provider": "twitter"
                    //}'
                    console.log('"oauth_token": "3354456526-6Nv5MDrhgwwKyVqgwFc15RYqJ4sj6FmAyx2z0R3"');
                    $rootScope.currentUser = false;
                }
            });

            return deferred.promise;
        },

        getUserData: function(){
            var oauth_token = this.isReady();
            if(oauth_token){
                // get user's data from token
                oauth_token.me().done(function(currentUser){
                    $rootScope.currentUser = currentUser;

                    // run the digest cycle to update scope with the 
                    // data we got from .me() oauth.io method
                    $rootScope.$apply();
                });
            } else {
                console.error('Cannot get user data. No one is logged in!');
                return false;
            }
        },
        clearCache: function() {
            // log them out and clear the scope
            OAuth.clearCache('twitter');
            $rootScope.currentUser = false;
        }
    };
});