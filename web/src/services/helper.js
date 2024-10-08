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

async function insert_picture(identifier, user) {
  const prisma = new PrismaClient();
  const timestamp = Math.floor(Date.now() / 1000)

  const picture = {
    picture_filename: identifier,
    user: {
      connect: {
        user_id: user.user_id,
      },
    },
    timestamp: timestamp,
  };
  try {
    await prisma.pictures.create({
      data: picture,
    });
    logger.info(`inserted picture for user: ${user.contact_name}`);
  }
  catch (e) {
    logger.error('Error inserting picture:', e);
  }
  prisma.$disconnect();
}

async function get_users() {
  try {
    const prisma = new PrismaClient();
    const db_users = await prisma.users.findMany({
      where: {
      },
    });
    prisma.$disconnect();
    return db_users;
  }
  catch (e) {
    logger.error('Error getting users:', e);
    throw e;
  }
}

module.exports = {
  pictureUrlToId,
  checkIfPictureNew,
  get_users,
  insert_picture,
};
