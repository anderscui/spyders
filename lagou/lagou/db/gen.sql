CREATE TABLE "main"."keyword" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "category" TEXT,
    "subcategory" TEXT,
    "encoded" TEXT,
    "created_on" TEXT NOT NULL,
    "updated_on" TEXT NOT NULL
);

CREATE TABLE "main"."position" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "pos_id" INTEGER NOT NULL,
  "name" TEXT NOT NULL,
  "create_time" TEXT NOT NULL,
  "city" TEXT NOT NULL,
  "salary" TEXT NOT NULL,
  "time_type" TEXT,
  "fin_stage" TEXT,
  "industry" TEXT,

  "category" TEXT,
  "subcategory" TEXT,

  "desc" TEXT NOT NULL,

  "leader" TEXT,
  "advantage" TEXT,

  "education" TEXT,
  "experience" TEXT,


  "com_id" INTEGER NOT NULL,
  "com_name" TEXT NOT NULL,
  "com_short_name" TEXT,
  "com_url" TEXT,
  "com_labels" TEXT,
  "com_logo" TEXT,
  "com_size" TEXT,
  "com_address" TEXT,

  -- meta data
  "created_on" TEXT NOT NULL,
  "updated_on" TEXT NOT NULL
);