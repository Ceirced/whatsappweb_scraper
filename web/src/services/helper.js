const { PrismaClient } = require("@prisma/client");
const pino = require('pino');

const logger = pino({ level: process.env.LOG_LEVEL || 'info' });

function pictureUrlToId(url) {
  const identifier = url.split("_n.jpg")[0].split("/").pop();
  return identifier;
}

async function checkIfAboutNew(about, user) {
  const prisma = new PrismaClient();
  const latest_about = await prisma.status.findFirst({
    where: {
      user: {
        user_id: user.user_id,
      },
    },
    orderBy: {
      timestamp: 'desc',
    },
    take: 1,
  });
  prisma.$disconnect();
  if (latest_about === null || latest_about.status === null) {
    if (about !== "") {
      logger.info(`${user.contact_name} added about: ${about}`);
      return true;
    }
    return false;
  }
  else {
    if (about === null) {
      logger.info(`${user.contact_name} removed about`);
      logger.debug(`latest about in db ${latest_about.status}`);
      return true;
    }
  }
  logger.debug(`latest about in db ${latest_about.status}`);
  return latest_about.status !== about;
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

async function insert_about(about, user) {
  const prisma = new PrismaClient();
  const timestamp = Math.floor(Date.now() / 1000)

  const status = {
    status: about,
    user: {
      connect: {
        user_id: user.user_id,
      },
    },
    timestamp: timestamp,
  };
  try {
    await prisma.status.create({
      data: status,
    });
    logger.info(`inserted about for user: ${user.contact_name}`);
  }
  catch (e) {
    logger.error('Error inserting about:', e);
  }
  prisma.$disconnect();
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
  checkIfAboutNew,
  insert_about
};
