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
            // console.log(response.data.rows);
            app.data.rows = response.data.rows
        });
    };

    app.set_follow = function (row_id) {
        console.log('set_follow() called')
        console.log('row id ' + row_id)

        // axios.post(set_follow_url).then(function() {
        //     console.log('in post')
        //     console.log(response);
        // });
        axios.post(set_follow_url,
            {
                id: row_id
            }).then(function (response) {
                console.log('in post');
                // console.log(response);
            });
    };

    // Have func to strip users out of rows?

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_users: app.get_users,
        set_follow: app.set_follow,
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
        // Put here any initialization code.
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it. 
console.log('Top level')
init(app);
