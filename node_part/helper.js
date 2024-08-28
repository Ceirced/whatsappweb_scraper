const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

function pictureUrlToId(url) {
  const identifier = url.split("_n.jpg")[0].split("/").pop();
  return identifier;
}

async function checkIfPictureNew(identifier) {
  const picture = await prisma.picture.findFirst({
    where: {
      picture_filename: identifier,
    },
  });
  return !picture;
}

module.exports = {
  pictureUrlToId,
  checkIfPictureNew,
};
