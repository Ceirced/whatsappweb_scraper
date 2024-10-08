const express = require('express');
const router = express.Router();
const profileController = require('../controllers/profileController');

// Define the route for getting new profile pictures
router.get('/scrape', profileController.scrapeProfilePictures);

module.exports = router;