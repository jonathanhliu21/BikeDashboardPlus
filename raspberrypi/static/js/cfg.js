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

class Cfg {
  // cfg class, represents a row in a table

  constructor(_nm, _desc, _val, _acpt) {
    this.name = _nm;
    this.description = _desc;
    this.value = _val;
    this.acpt = _acpt;

    for (let i = 0; i < this.acpt.length; i++) {
      this.acpt[i] = this.acpt[i].toString();
    }
  }
}

axios
  .get("/tzs/raw")
  .then((res) => {
    // hard coded configurations
    const cfgs = [
      new Cfg(
        "LED",
        "This value indicates how the speed should be displayed on the LED matrix. If the value is 0, then each LED represents 1 unit of speed. If the value is 1, then each LED represents 2 units of speed. For example, if your current speed was 4 miles per hour, then 4 LEDs would light up if LED=0 and 2 LEDs would light up if LED=1. The value must be either 0 or 1.",
        0,
        [0, 1]
      ),
      new Cfg(
        "DTM",
        "This value indicates how the date should be shown. If it is 0, then the date is shown MM-DD. If it is 1, then it is shown DD-MM. The value must be either 0 or 1",
        0,
        [0, 1]
      ),
      new Cfg(
        "TMZ",
        "Your time zone. Must be a valid name from the tz database.",
        "America/Los_Angeles",
        res.data
      ),
      new Cfg(
        "UNT",
        "The unit of speed you use. If the value is 0, then mph is used. If the value is 1, kph is used. If the value is 2, m/s is used. Value must be 0, 1, or 2.",
        0,
        [0, 1, 2]
      ),
      new Cfg(
        "24H",
        "Indicates whether you use a 24 hour clock. If it is 0, it will show a 12 hour clock with AM and PM at the end(1:00PM instead of 13:00). If the value is 1, then the clock will show from 00:00-23:00. Value must be 0 or 1.",
        0,
        [0, 1]
      ),
    ];

    // put configs on DOM
    new Vue({
      el: "#cfg-table",
      delimiters: ["[[", "]]"],
      data: {
        cfgs: cfgs,
        msg: ["", "", "", "", ""],
      },
      computed: {
        allSatisfy: function () {
          // checks that all values are in range before letting user submit
          // prevents error in python when in bike mode
          for (let i = 0; i < this.cfgs.length; i++) {
            if (!this.cfgs[i].acpt.includes(this.msg[i])) return true;
          }
          return false;
        },
      },
    });
  })
  .catch((err) => {
    console.log(err);
  });
