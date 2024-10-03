const { PrismaClient } = require("@prisma/client");
const fs = require("fs");
const prisma = new PrismaClient();

function pictureUrlToId(url) {
  const identifier = url.split("_n.jpg")[0].split("/").pop();
  return identifier;
}

async function checkIfPictureNew(identifier) {
  const picture = await prisma.pictures.findFirst({
    where: {
      picture_filename: identifier,
    },
  });
  return !picture;
}

function get_users() {
  users = JSON.parse(fs.readFileSync("node_users.json", "utf8"));
  return users;
}

module.exports = {
  pictureUrlToId,
  checkIfPictureNew,
  get_users,
};
