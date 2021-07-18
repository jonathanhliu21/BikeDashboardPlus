function main(sz){
    sz = parseInt(sz);

    var app = new Vue({
        el: "#combine_pg",
        delimiters: ["[[", "]]"],
        data: {
            checked_: []
        },
        methods: {
            post_cmb: function(){
                var order = this.checked_.join(", ");
                var cfm = confirm(`Are you SURE that you want to combine the files in this order: ${order}? Note that this action is IRREVERSIBLE and the files CANNOT be separated again after you press OK`);

                if (cfm) {
                    axios.post("/map/combine", {
                        "files": this.checked_
                    })
                    .then(
                        (response) => {
                            if (response.status == 200){
                                alert("Successfully combined files");
                                window.location.href = "/map";
                            }
                        } 
                    )
                    .catch(
                        (err) => {
                            console.log(err);
                        }
                    );
                } else {
                    this.checked_ = [];
                }
            }
        },
    });
}

