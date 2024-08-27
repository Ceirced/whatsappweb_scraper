-- CreateTable
CREATE TABLE "User" (
    "user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "contact_name" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Picture" (
    "image_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "picture_filename" TEXT NOT NULL,
    "timestamp" BIGINT NOT NULL,
    "user_id" INTEGER NOT NULL,
    CONSTRAINT "Picture_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Status" (
    "status_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "status" TEXT NOT NULL,
    "timestamp" BIGINT NOT NULL,
    "user_id" INTEGER NOT NULL,
    CONSTRAINT "Status_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "User_contact_name_key" ON "User"("contact_name");

-- CreateIndex
CREATE UNIQUE INDEX "Picture_picture_filename_timestamp_user_id_key" ON "Picture"("picture_filename", "timestamp", "user_id");

-- CreateIndex
CREATE UNIQUE INDEX "Status_status_timestamp_user_id_key" ON "Status"("status", "timestamp", "user_id");
