const qrcode = require("qrcode-terminal");
const pino = require('pino');
const axios = require('axios');
const path = require('path');
const fs = require('fs');
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });
const { Client, LocalAuth } = require("whatsapp-web.js");
const { pictureUrlToId, checkIfPictureNew, get_users, insert_picture, checkIfAboutNew, insert_about } = require("./helper");


const scrapeNewProfilePictures = async () => {
    const whatsapp = new Client({
        puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] },
        authStrategy: new LocalAuth(
            {
                dataPath: './src/services/sessions'
            }
        ),
    });
    whatsapp.on("qr", (qr) => {
        qrcode.generate(qr, {
            small: true,
        });
    });


    whatsapp.on('loading_screen', (percent, message) => {
        logger.info('LOADING SCREEN:', percent, message);
    });

    whatsapp.on('ready', async () => {
        logger.info('READY');
        const debugWWebVersion = await whatsapp.getWWebVersion();
        logger.debug(`WWebVersion = ${debugWWebVersion}`);

        await processContacts(whatsapp);

        whatsapp.pupPage.on('pageerror', function (err) {
            console.log('Page error: ' + err.toString());
        });
        whatsapp.pupPage.on('error', function (err) {
            console.log('Page error: ' + err.toString());
        });

        whatsapp.destroy();
    });
    whatsapp.initialize();
}

async function processContacts(whatsapp) {
    try {
        logger.info('Processing contacts');
        const contacts = await whatsapp.getContacts();
        const users = await get_users();
        logger.info(`Processing ${users.length} users`);

        for (const user of users) {
            const contact = contacts.find((contact) => contact.name === user.contact_name);
            if (contact) {
                const new_picture = await checkProfilePicture(whatsapp, contact);
                const new_about = await checkAbout(contact, user);

                if (new_about) {
                    logger.info(`New about for ${contact.name} detected!`);
                    // Save the about to the database
                    await insert_about(new_about, user);
                }

                if (new_picture) {
                    const url = await whatsapp.getProfilePicUrl(contact.id._serialized);
                    const picture_id = pictureUrlToId(url);
                    await insert_picture(picture_id, user);
                    await download_picture(url, contact);
                }

            }
        }
    } catch (error) {
        logger.error("Error processing contacts:", error);
        throw error;
    }
}

async function download_picture(url, contact) {
    try {
        const response = await axios({
            url,
            method: 'GET',
            responseType: 'stream'
        });

        const picture_id = pictureUrlToId(url);
        const dirPath = path.join('images', contact.name);

        // Ensure the directory exists
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }

        const filePath = path.join(dirPath, `${contact.name}_${picture_id}.jpg`);

        return new Promise((resolve, reject) => {
            response.data.pipe(fs.createWriteStream(filePath))
                .on('finish', () => resolve())
                .on('error', (e) => reject(e));
        });
    } catch (error) {
        logger.error("Error downloading picture:", error);
        throw error;
    }
}

async function checkAbout(contact, user) {
    try {
        const about = await contact.getAbout();
        const isNew = await checkIfAboutNew(about, user);
        if (isNew) {
            return about;
        } else {
            return false;
        }
    } catch (error) {
        logger.error(`Error checking about for ${contact.name}`, error);
        throw error;
    }
}

// Check if the profile picture is new
async function checkProfilePicture(whatsapp, contact) {
    try {
        const url = await whatsapp.getProfilePicUrl(contact.id._serialized);
        if (!url) {
            logger.info(`No profile picture found for ${contact.name}`);
            return;
        }
        const picture_id = pictureUrlToId(url);
        const isNew = await checkIfPictureNew(picture_id);

        if (isNew) {
            logger.info(`New profile picture for ${contact.name} detected!`);
            // Save the picture to the database
            return true;
        } else {
            logger.info(`Profile picture not changed for ${contact.name}`);
            return false;
        }
    } catch (error) {
        logger.error(`Error checking profile picture for ${contact.name}`, error);
    }
}


module.exports = { scrapeNewProfilePictures, }