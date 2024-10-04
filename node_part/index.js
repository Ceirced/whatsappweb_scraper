const qrcode = require("qrcode-terminal");
const pino = require('pino');
const { Client, LocalAuth } = require("whatsapp-web.js");
const whatsapp = new Client({
  authStrategy: new LocalAuth(),
});

const { pictureUrlToId, checkIfPictureNew, get_users } = require("./helper");

const express = require("express");
const app = express();
const port = 3000;

const logger = pino({ level: process.env.LOG_LEVEL || 'info' });

// whatsapp
whatsapp.on("qr", (qr) => {
  qrcode.generate(qr, {
    small: true,
  });
});


whatsapp.on('loading_screen', (percent, message) => {
  logger.info('LOADING SCREEN', percent, message);
});

whatsapp.on('ready', async () => {
  logger.info('READY');
  const debugWWebVersion = await whatsapp.getWWebVersion();
  logger.debug(`WWebVersion = ${debugWWebVersion}`);

  await processContacts();

  whatsapp.pupPage.on('pageerror', function (err) {
    console.log('Page error: ' + err.toString());
  });
  whatsapp.pupPage.on('error', function (err) {
    console.log('Page error: ' + err.toString());
  });

  whatsapp.destroy();
});

// Process contacts and check for new profile pictures
async function processContacts() {
  try {
    const contacts = await whatsapp.getContacts();
    const users = await get_users();

    for (const user of users) {
      const contact = contacts.find((contact) => contact.name === user.contact_name);
      if (contact) {
        await checkProfilePicture(contact);
      }
    }
  } catch (error) {
    logger.error("Error processing contacts:", error);
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


whatsapp.initialize();
