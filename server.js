const express = require('express')
const session = require('express-session')
const bodyParser = require('body-parser')
const router = express.Router();
const app = express();
const mongoose = require('mongoose')

mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost:27017/accounts', {useNewUrlParser: true});

var userSchema = new mongoose.Schema({
	username: String,
	password: String,
	email: String,
	role: String
});
var User = mongoose.model('User', userSchema);

//Pthon related
const spawn = require("child_process").spawn;
//const pythonProcess = spawn('python',["path/to/script.py", arg1, arg2, ...]);

app.use(session({secret: 'ssshhhhh', saveUninitialized: true, resave: true}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + '/views'));

var sess;
// app.get('/', function(req, res) {
// 	sess = req.session;
// 	sess.username;
// });

router.get('/', (req, res) => {
	sess = req.session;
	if(sess.username) {
		res.redirect('/admin');
	}
	res.sendFile(__dirname + '/views/HTML/Register.html');
});

router.post('/login', (req, res) => {
	sess = req.session;
	sess.username = req.body.username; //might be username-input instead
	res.end('done');
});

router.get('/admin', (req, res) => {
	sess = req.session;
	if(sess.username) {
		// res.write(`<h1>Hello ${sess.username} </h1><br>`);
		// res.end('<a href='+'/logout'+'>Logout</a>');
		res.sendFile(__dirname + '/views/HTML/Apriori.html');
	}
	else {
		res.write('<h1>Please log in first</h1>');
		res.end('<a href='+'/'+'>Login</a>');
	}
});

router.get('/logout', (req, res) => {
	req.session.destroy((err) => {
		if(err) {
			return console.log(err);
		}
		res.redirect('/');
	});
});

// Register.html functions
//FUNCTION FOR REGISTER IN Register.html
router.post("/register", (req, res) => {
	User.findOne({username: req.query.username}, function(err, user) {
		if(err) {console.log(err);}
		var message;
		if(user) {
			message = "User already exists";
			console.log(message);
			return false;
		}
		else {
			var user = new User({
				username: req.body.username,
				password: req.body.password,
				email: req.body.email,
				role: req.body.role
			});
			console.log("Successfully created user");
			user.save(function (err) {
				if(err) {console.log(err);}
				alert("User Created");
				res.sendFile(__dirname + '/views/HTML/ViewUsers.html');
			})
		}
	});
});


//Apriori.html functions
//FUNCTION FOR APRIORI ALGORITHM

//TEST FUNCTION FOR IMPORTING THE PYTHON SCRIPT
router.post("/aprioriAlgo" , (req, res) => {
	const test = spawn("python", ["Python/python.py" , "a", "b", "c"])
	test.stdout.on("data", function(data){
		console.log(data.toString());
		res.write(data);
		res.end("end");
	});
	//console.log(req.body);
});


// router.post("aprioriAlgo" , (req, res) =>{
// 	const algorithm = spawn("python", [Python/python.py, ])
// 	test.stdout.on("data" , function(data){
// 		console.long(data.toString());
// 		res.write(data)
// 		res.end();
// 	});
// });

app.use('/', router);

app.listen(process.env.PORT || 3000, () => {
	console.log(`App Started on PORT ${process.env.PORT || 3000}`);
});
