const { PrismaClient } = require("@prisma/client");
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

async function get_users() {
  const db_users = await prisma.users.findMany({
    take: 20,
  });
  return db_users;
}

module.exports = {
  pictureUrlToId,
  checkIfPictureNew,
  get_users,
};
