const express = require('express')
const app = express()
const morgan = require('morgan')
const port = 3000

//settings
app.set('port', process.env.PORT || 3000)

//middlewares
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());


//routes
app.use(require('./routes/procesador'))


//start the server
app.listen(app.get('port'), () => console.log(`Server on port ${app.get('port')}`));