const qrcode = require("qrcode-terminal");
const pino = require('pino');
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });
const { Client, LocalAuth } = require("whatsapp-web.js");
const { pictureUrlToId, checkIfPictureNew, get_users, insert_picture } = require("./helper");


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
        logger.info('LOADING SCREEN:::', percent, message);
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
                const new_picture = await checkProfilePicture(contact);
                if (new_picture) {
                    const url = await whatsapp.getProfilePicUrl(contact.id._serialized);
                    const picture_id = pictureUrlToId(url);
                    // await insert_picture(picture_id, user);
                }

            }
        }
    } catch (error) {
        logger.error("Error processing contacts:", error);
        throw error;
    }
}

// Check if the profile picture is new
async function checkProfilePicture(contact) {
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