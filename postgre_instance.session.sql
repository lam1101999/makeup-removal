CREATE TABLE "author"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "data_of_birth" DATE NOT NULL
);
ALTER TABLE "author"
ADD PRIMARY KEY("id");
CREATE TABLE "profile"(
    "email" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "phone_number" VARCHAR(255) NOT NULL,
    "date_of_birth" DATE NOT NULL
);
ALTER TABLE "profile"
ADD PRIMARY KEY("email");
CREATE TABLE "publisher"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "publisher"
ADD PRIMARY KEY("id");
CREATE TABLE "account"(
    "id" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "role_id" BIGINT NOT NULL,
    "email" VARCHAR(255) NOT NULL
);
ALTER TABLE "account"
ADD PRIMARY KEY("id");
ALTER TABLE "account"
ADD CONSTRAINT "account_email_unique" UNIQUE("email");
CREATE TABLE "account_book"(
    "book_id" BIGINT NOT NULL,
    "account_id" VARCHAR(255) NOT NULL,
    "borrow_date" DATE NOT NULL,
    "return_date" DATE NOT NULL
);
CREATE INDEX "account_book_book_id_account_id_borrow_date_index" ON "account_book"(
    "book_id",
    "account_id",
    "borrow_date"
);
CREATE INDEX "account_book_book_id_index" ON "account_book"("book_id");
CREATE INDEX "account_book_account_id_index" ON "account_book"("account_id");
CREATE INDEX "account_book_borrow_date_index" ON "account_book"("borrow_date");
CREATE TABLE "book_author"(
    "book_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL
);
CREATE INDEX "book_author_book_id_author_id_index" ON "book_author"("book_id", "author_id");
CREATE INDEX "book_author_book_id_index" ON "book_author"("book_id");
CREATE INDEX "book_author_author_id_index" ON "book_author"("author_id");
CREATE TABLE "profile_adress"(
    "adress_id" BIGINT NOT NULL,
    "email" VARCHAR(255) NULL
);
CREATE INDEX "profile_adress_adress_id_email_index" ON "profile_adress"("adress_id", "email");
CREATE INDEX "profile_adress_adress_id_index" ON "profile_adress"("adress_id");
CREATE INDEX "profile_adress_email_index" ON "profile_adress"("email");
CREATE TABLE "category"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "category"
ADD PRIMARY KEY("id");
CREATE TABLE "role"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE "role"
ADD PRIMARY KEY("id");
CREATE TABLE "book"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "year" BIGINT NOT NULL,
    "publisher_id" BIGINT NOT NULL
);
ALTER TABLE "book"
ADD PRIMARY KEY("id");
CREATE TABLE "book_category"(
    "category_id" BIGINT NOT NULL,
    "book_id" BIGINT NOT NULL
);
CREATE INDEX "book_category_category_id_book_id_index" ON "book_category"("category_id", "book_id");
CREATE INDEX "book_category_category_id_index" ON "book_category"("category_id");
CREATE INDEX "book_category_book_id_index" ON "book_category"("book_id");
CREATE TABLE "address"(
    "id" BIGINT NOT NULL,
    "unit_number" INTEGER NOT NULL,
    "street" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL
);
ALTER TABLE "address"
ADD PRIMARY KEY("id");
ALTER TABLE "book"
ADD CONSTRAINT "book_publisher_id_foreign" FOREIGN KEY("publisher_id") REFERENCES "publisher"("id");
ALTER TABLE "account"
ADD CONSTRAINT "account_email_foreign" FOREIGN KEY("email") REFERENCES "profile"("email");
ALTER TABLE "book_author"
ADD CONSTRAINT "book_author_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE "profile_adress"
ADD CONSTRAINT "profile_adress_email_foreign" FOREIGN KEY("email") REFERENCES "profile"("email");
ALTER TABLE "account_book"
ADD CONSTRAINT "account_book_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE "account_book"
ADD CONSTRAINT "account_book_account_id_foreign" FOREIGN KEY("account_id") REFERENCES "account"("id");
ALTER TABLE "book_category"
ADD CONSTRAINT "book_category_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE "book_author"
ADD CONSTRAINT "book_author_author_id_foreign" FOREIGN KEY("author_id") REFERENCES "author"("id");
ALTER TABLE "account"
ADD CONSTRAINT "account_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "role"("id");
ALTER TABLE "book_category"
ADD CONSTRAINT "book_category_category_id_foreign" FOREIGN KEY("category_id") REFERENCES "category"("id");
ALTER TABLE "profile_adress"
ADD CONSTRAINT "profile_adress_adress_id_foreign" FOREIGN KEY("adress_id") REFERENCES "address"("id");