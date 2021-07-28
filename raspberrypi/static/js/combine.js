/*
MIT License

Copyright (c) 2021 jonyboi396825

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

*/

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

