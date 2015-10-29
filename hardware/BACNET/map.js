var parse = require('csv-parse'),
    fs = require('fs'),
    Q = require('q'),
    deferred = Q.defer();




    //asuming pointArr from readpropm will be [name, value]

var mapper = function(pointArr) {
    fs.readFile('Park345.csv', function(err, data) {
        parse(data, function(err, map) {
            for (var i = 0; i < map.length; i++) {
                if (map[i][4] == pointArr[0]) {
                     deferred.resolve(map[i])
                }
            }
        })
    })

    return deferred.promise
};


// mapper(['HouseTank45High', 345]).then(function(data){
// 	console.log(data)
// })


var regexTest = function(){
	var pattern = /\b(List of Objects in Test Device:)\b/mgi
	fs.readFile('345_Master_Points.txt', function(err,data){
		// console.log(data.toString())
		var match = pattern.exec(data.toString());
		console.log(match);
	})
}

regexTest();
// module.exports = {
// 	mapper: mapper
// };

