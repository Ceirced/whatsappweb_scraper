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


whatsapp.on("ready", () => {
  console.log("Client is ready!");
  whatsapp
    .getContacts()
    .then((contacts) => {
      const users = get_users();
      users.then((users) => {
        users.forEach((user) => {
          const contact = contacts.find((contact) => contact.name === user.contact_name);
          if (contact) {
            whatsapp.getProfilePicUrl(contact.id._serialized).then((url) => {
              picture_id = pictureUrlToId(url);
              checkIfPictureNew(picture_id).then((isNew) => {
                if (isNew) {
                  console.log("New profile picture detected!");
                } else {
                  console.log("Profile picture not changed for user:", contact.name);
                }
              });
            });
          } else {
            console.log("Contact not found:", user.name);
          }
        });
      });
    })
    .catch((error) => {
      console.error("Error fetching contacts:", error);
    });
})


whatsapp.initialize();
