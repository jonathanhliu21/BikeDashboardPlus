axios.get("/tzs/raw")
.then((res) => {

    new Vue({
        el: "#tz-list",
        delimiters: ["[[", "]]"],
        data: {
            search_tz: "",
            all_tzs: res.data,
        },
        methods: {
            check_match: function(i){
                let i_cpy = i.replace(/[^0-9a-z]/gi, '');
                let srch_cpy = this.search_tz.replace(/[^0-9a-z]/gi, '');
                
                return (this.search_tz === "" || (i_cpy.toLowerCase().substring(0, srch_cpy.length) === srch_cpy.toLowerCase()));
            }
        }
    });
})
.catch((err) => {
    console.log(err);
});
    