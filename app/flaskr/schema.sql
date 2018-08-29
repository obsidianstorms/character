DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS game;

CREATE TABLE user (
  id integer PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE game (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  play_date TEXT NOT NULL,
  adventure_name TEXT NOT NULL,
  adventure_code TEXT NOT NULL,
  session_number TEXT NOT NULL,
  gm_name TEXT NOT NULL,
  gm_dci TEXT NOT NULL,
  experience INTEGER NOT NULL,
  ap INTEGER NOT NULL,
  gold FLOAT NOT NULL,
  magic_count INTEGER NOT NULL,
  tier1_tp INTEGER NOT NULL,
  tier2_tp INTEGER NOT NULL,
  tier3_tp INTEGER NOT NULL,
  tier4_tp INTEGER NOT NULL,
  renown INTEGER NOT NULL,
  downtime INTEGER NOT NULL,
  story_awards TEXT NOT NULL,
  acquired_items TEXT NOT NULL,
  removed_items TEXT NOT NULL,
  downtime_activity TEXT NOT NULL,
  notes TEXT NOT NULL,
  FOREIGN KEY (player_id) references user (id)
);

CREATE TABLE bag (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  character_id INTEGER NOT NULL,
  contents TEXT NOT NULL,
  FOREIGN KEY (character_id) references user (id)
);

