-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

-- Create the database and tables
CREATE DATABASE tournament;

\c tournament;
-- players: id, name
CREATE TABLE players(
  id SERIAL PRIMARY KEY,
  name TEXT
);

-- matches: winner, loser
CREATE TABLE matches(
  winner INTEGER references players(id),
  loser INTEGER references players(id),
  PRIMARY KEY (winner, loser)
);

-- Create a view that tallies total matches per player
-- References: https://discussions.udacity.com/t/tournament-results-database/211977/7
CREATE VIEW standings AS
	SELECT players.id,players.name,
                (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner) AS wins,
		(SELECT COUNT(*) FROM matches WHERE players.id = matches.winner OR players.id = matches.loser) AS matches
	FROM players
        ORDER BY wins DESC;

