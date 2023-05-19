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
        results: [],
        rows: [],
        following: [],
        searching: false,
        row_len: 0
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
            app.data.row_len = app.data.rows.length
        });
    };

    app.get_following = function() {
        axios.get(get_following_url).then(function(response) {
            console.log("IN GET FOLLOWING: " + response.data.following)
            app.data.following = response.data.following
            console.log("LENGT", app.data.row_len)

            // console.log('FOLLOWING ID: ' + app.data.foll[0]['following_id']);
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


    app.set_unfollow = function (row_id) {
        axios.post(set_unfollow_url,
            {
                id: row_id
            }
            ).then(function (response) {
            app.get_following()
        });
    }


    app.is_following = function(id) {
        console.log("Searching for " + id + "in list");

        // if (id in app.data.following) {
        // if (app.data.following.includes(id)) {
        //     console.log(id +'in list')
        //     return true;
        // }

        console.log('db', app.data.following[0]);
        // for (follower in app.data.following) {
        for (ind = 0; ind < app.data.following.length; ind += 1) {
            console.log('Follower: ' + app.data.following[ind]['following_id']);
            // if (id == app.data.following[ind['following_id']]) {
            if (id == app.data.following[ind]['following_id']) {
                console.log('IT EXISTS!');
                return true;
            }
        }

        console.log('test',app.data.following)

        console.log(id + " Not in list");

        return false;
    };


    app.search = function () {
        app.data.searching = true
        console.log("SEARCH")
        console.log("QUEURY:", app.vue.query)
        if (app.data.query.length >= 1) {
            axios.get(search_url, {params: {q: app.data.query}})
            .then(function (result) {
                // console.log("RES:", result.data.results['username'])

                app.data.results = result.data.results;
            });
        } else {
            // app.data.results = [];
            app.clear_search()
        }
    }

    app.clear_search = function () {
        app.data.searching = false
        app.data.query = ""
        app.data.results = []
    }


    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_users: app.get_users,
        get_following: app.get_following,
        set_follow: app.set_follow,
        set_unfollow: app.set_unfollow,
        is_following: app.is_following,
        search: app.search,
        clear_search: app.clear_search,
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
        // app.search()
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
