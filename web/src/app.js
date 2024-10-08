const express = require('express');
const bodyParser = require('body-parser');
const profileRoutes = require('./api/profile');  // Import the routes

const app = express();

// Routes
app.use('/api/profile', profileRoutes);  // Define the base route for profile

// Error Handling (optional)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

module.exports = app;