var fs = require('fs');
var express = require('express');
var http = require('http');
var path = require('path');

fs.readFile('./index.html', function (err, html) {
	if (err) {
        throw err;
	}

    var app = express();

    app.get('/', function(req, res) {
        res.writeHeader(200, {'Content-Type' : 'text/html' });
        res.write(html);
        res.end();
    });

    app.get('/currenttemp', function(req, res) {
        fs.readFile('./currenttemp.txt', function(err, content) {
            if (err) {
                throw err;
            }

            res.writeHeader(200, {'Content-Type' : 'text/plain' });
            res.write(content);
            res.end();
        });
    });

    app.get('/runningstatus', function(req, res) {
        fs.readFile('./runningstatus.txt', function(err, content) {
            if (err) {
                throw err;
            }

            res.writeHeader(200, {'Content-Type' : 'text/plain' });
            res.write(content);
            res.end();
        });
    });

    var port = 3000;
    var ipAddress = '192.168.1.5';

    app.set('port', port);
    app.set('ipAddress', ipAddress);

    app.use(express.static(path.join(__dirname, 'public')));

    var server = http.createServer(app);
    server.listen(port, ipAddress);

    console.log('NodeJS server running at http://%s:%s', ipAddress, port);
});