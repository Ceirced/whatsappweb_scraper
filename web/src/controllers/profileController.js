// src/controllers/profileController.js
const whatsappService = require('../services/whatsappService');

// Controller function to handle the scraping of WhatsApp profile pictures
const scrapeProfilePictures = async (req, res) => {
    try {
        const profilePics = await whatsappService.scrapeNewProfilePictures();  // Service layer handles scraping logic
        res.status(200).json({ success: true, data: profilePics });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, message: 'Failed to scrape profile pictures' });
    }
};

module.exports = {
    scrapeProfilePictures,
};
