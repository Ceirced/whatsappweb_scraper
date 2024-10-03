const qrcode = require("qrcode-terminal");
const { Client, LocalAuth } = require("whatsapp-web.js");
const whatsapp = new Client({
  authStrategy: new LocalAuth(),
});

const { pictureUrlToId, checkIfPictureNew, get_users } = require("./helper");

const express = require("express");
const app = express();
const port = 3000;

// whatsapp
whatsapp.on("qr", (qr) => {
  qrcode.generate(qr, {
    small: true,
  });
});


// Log when the client is ready
whatsapp.on("ready", async () => {
  console.log("Client is ready!");
  await processContacts();
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
    console.error("Error processing contacts:", error);
  }
}

// Check if the profile picture is new
async function checkProfilePicture(contact) {
  try {
    const url = await whatsapp.getProfilePicUrl(contact.id._serialized);
    const picture_id = pictureUrlToId(url);
    const isNew = await checkIfPictureNew(picture_id);

    if (isNew) {
      console.log("New profile picture detected!");
    } else {
      console.log("Profile picture not changed for user:", contact.name);
    }
  } catch (error) {
    console.error("Error checking profile picture:", error);
  }
}


whatsapp.initialize();
