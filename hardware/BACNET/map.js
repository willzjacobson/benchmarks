var parse = require('csv-parse'),
    fs = require('fs')




var spreadsheet = function() {
        fs.readFile('Park345.csv', function(err, data) {
            parse(data, function(err, data) {
                return data;
            })
        })
    }
    //asuming pointArr from readpropm will be [name, value]

var mapper = function(pointArr) {
    var maparr = spreadsheet();
    for (var i = 0; i < maparr.length; i++) {
        if (maparr[i][4] == pointArr[0]) {
            return {
                "buildingRoute": mapparr[i][0],
                "BMSPointName": mapparr[i][1],
                "Master": mapparr[i][2],
                "Controller": mapparr[i][3],
                "PointName": mapparr[i][4],
                "System": mapparr[i][5],
                "System display name": mapparr[i][6],
                "Description": mapparr[i][7],
                "Units": mapparr[i][8],
                "Sample": mapparr[i][9]
            }
        }
    }
};




// module.exports = {
// 	mapper: mapper
// };
