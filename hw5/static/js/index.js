// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        query: "",
        rows: [],
        following: [],
        // foll: [],
    };    
    
    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };    


    // app.follow = funct () {
    //  axios.post(set_follow_url).then(function(response)) {
        // console.log(response)
        // app.data.query =

    // }


    app.get_users = function() {
        // app.data.rows = []
        // console.log(app.data.rows)
        console.log('top of get_user()')
        axios.get(get_users_url).then(function(response) {
            console.log('rows' + response.data.rows);
            app.data.rows = response.data.rows
        });
    };

    app.get_following = function() {
        axios.get(get_following_url).then(function(response) {
            console.log("IN GET FOLLOWING: " + response.data.following)
            app.data.foll = response.data.following
            console.log('FOLLOWING ID: ' + app.data.foll[0]['following_id']);
        })
    }

    app.set_follow = function (row_id) {
        console.log('set_follow() called')
        console.log('row id ' + row_id)
        // app.data.following.push(row_id)
        console.log(app.data.following)

        // axios.post(set_follow_url).then(function() {
        //     console.log('in post')
        //     console.log(response);
        // });
        axios.post(set_follow_url,
            {
                id: row_id
            }).then(function (response) {
                console.log('in post');
                console.log('Now adding ' + row_id + ' to following_list');
                app.get_following()
                console.log('now: ' + app.data.following)
                
                // console.log(response);
            });
    };

    // Have func to strip users out of rows?


    app.is_following = function(id) {
        console.log("Searching for " + id + "in list");

        // if (id in app.data.following) {
        // if (app.data.following.includes(id)) {
        //     console.log(id +'in list')
        //     return true;
        // }

        console.log('test',app.data.following)

        console.log(id + " Not in list");

        return false;
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_users: app.get_users,
        get_following: app.get_following,
        set_follow: app.set_follow,
        is_following: app.is_following,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        console.log("Top of init()")
        app.get_users()
        app.get_following()
        // app.data.foll = response.data.following
        // console.log('folling ' + app.data.foll)
        // Put here any initialization code.
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it. 
console.log('Top level')
init(app);
