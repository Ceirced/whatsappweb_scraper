const { PrismaClient } = require("@prisma/client");
const pino = require('pino');

const logger = pino({ level: process.env.LOG_LEVEL || 'info' });

function pictureUrlToId(url) {
  const identifier = url.split("_n.jpg")[0].split("/").pop();
  return identifier;
}

async function checkIfPictureNew(identifier) {
  const prisma = new PrismaClient();
  const picture = await prisma.pictures.findFirst({
    where: {
      picture_filename: identifier,
    },
  });
  prisma.$disconnect();
  return !picture;
}

async function get_users() {
  const prisma = new PrismaClient();
  const db_users = await prisma.users.findMany({
    where: {
    },
  });
  prisma.$disconnect();
  return db_users;
}

module.exports = {
  pictureUrlToId,
  checkIfPictureNew,
  get_users,
};
