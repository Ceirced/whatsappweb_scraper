const qrcode = require("qrcode-terminal");
const fs = require("fs");
const { Client, LocalAuth } = require("whatsapp-web.js");
const whatsapp = new Client({
  authStrategy: new LocalAuth(),
});

const { pictureUrlToId, checkIfPictureNew } = require("./helper");

const express = require("express");
const app = express();
const port = 3000;

// whatsapp
whatsapp.on("qr", (qr) => {
  qrcode.generate(qr, {
    small: true,
  });
});

const users = JSON.parse(fs.readFileSync("node_users.json", "utf8"));

whatsapp.on("ready", () => {
  console.log("Client is ready!");
  whatsapp
    .getContacts()
    .then((contacts) => {
      // get the profile picture of the contacts in the users.json file
      users.users.forEach((user) => {
        const contact = contacts.find((contact) => contact.name === user.name);
        if (contact) {
          console.log("Contact found:", contact.name);
          whatsapp.getProfilePicUrl(contact.id._serialized).then((url) => {
            console.log("Profile picture URL:", pictureUrlToId(url));
            checkIfPictureNew(pictureUrlToId(url)).then((isNew) => {
              if (isNew) {
                console.log("New profile picture detected!");
              } else {
                console.log("Profile picture not changed.");
              }
            });
          });
        } else {
          console.log("Contact not found:", user.name);
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching contacts:", error);
    });
});

whatsapp.initialize();