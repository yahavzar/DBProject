
create TABLE IF NOT EXISTS Movie(
apiId int PRIMARY KEY,
title varchar(128),
langId int,
releaseDay DATETIME,
length int,
budget bigint,
revenue bigint,
collection varchar(128),
imdbId varchar(16),
homePage varchar(256),
status varchar(32),
popularity float,
voteCount int,
voteAvg float,
adult boolean
);

create TABLE IF NOT EXISTS Genre(
genreId int PRIMARY KEY,
genreName varchar(32)
);

create TABLE IF NOT EXISTS Language(
languageId int PRIMARY KEY,
languageName varchar(32)
);

create TABLE IF NOT EXISTS Actors(
actorId int PRIMARY KEY,
actorName varchar(64),
gender int
);


create TABLE IF NOT EXISTS MoviesGenre(
genreId int,
apiId int
PRIMARY key (genreId,apiId)


);

create TABLE IF NOT EXISTS LanguageMovie(
languageId int,
movieId int
PRIMARY key (languageId,movieId)

);

create TABLE IF NOT EXISTS Directors(
directorId int PRIMARY KEY,
directorName varchar(32)
);

create TABLE IF NOT EXISTS ActorsMovie(
actorId int,
filmId int
PRIMARY key (actorId,filmId)

);

create TABLE IF NOT EXISTS DirectorsMovie(
directorId int,
filmId int
PRIMARY key (directorId,filmId)
);

create TABLE IF NOT EXISTS MovieOverview(
filmId int PRIMARY KEY,
overview varchar(1024)
);

create TABLE IF NOT EXISTS Shows(
apiId int PRIMARY KEY,
title varchar(128),
langId int,
releaseDay DATETIME,
length int,
homePage varchar(256),
status varchar(32),
popularity float,
voteCount int,
voteAvg float,
seasons int,
lastEpisodeId int,
nextEpisodeId int
);

create TABLE IF NOT EXISTS ShowGenre(
genreId int,
apiId int
PRIMARY key (genreId,apiId)

);

create TABLE IF NOT EXISTS LanguageShow(
languageId int,
showId int
PRIMARY key (languageId,showId)

);

create TABLE IF NOT EXISTS Producers(
producerId int PRIMARY KEY,
producerName varchar(32)
);

create TABLE IF NOT EXISTS ActorsShow(
actorId int,
showId int,
PRIMARY key (actorId,showId)
);

create TABLE IF NOT EXISTS ProducersShow(
producerId int,
showId int,
PRIMARY key (producerId,showId)

);

create TABLE IF NOT EXISTS ShowOverview(
showId int PRIMARY KEY,
overview varchar(2048)
);

CREATE TABLE IF NOT EXISTS PosterShow(
    apiId int NOT NULL PRIMARY KEY,
    image VARCHAR(64)
   );

   CREATE TABLE IF NOT EXISTS PosterMovie(
    apiId int NOT NULL PRIMARY KEY,
    image VARCHAR(64)
   );
--====================================================================================================================--
-- 2) Adding foreign keys
--====================================================================================================================--
ALTER TABLE ActorsMovie
ADD FOREIGN KEY (actorId) REFERENCES Actors(actorId);

ALTER TABLE ActorsShow
ADD FOREIGN KEY (actorId) REFERENCES Actors(actorId);

ALTER TABLE DirectorsMovie
ADD FOREIGN KEY (directorId) REFERENCES Directors(directorId);

ALTER TABLE DirectorsMovie
ADD FOREIGN KEY (filmId) REFERENCES Movie(apiid);



ALTER TABLE LanguageMovie
ADD FOREIGN KEY (languageId) REFERENCES Language(languageId);

ALTER TABLE LanguageShow
ADD FOREIGN KEY (showId) REFERENCES Shows(apiId);

ALTER TABLE LanguageShow
ADD FOREIGN KEY (languageId) REFERENCES Language(languageId);

ALTER TABLE Movie
ADD FOREIGN KEY (langId) REFERENCES Language(languageId);

ALTER TABLE Shows
ADD FOREIGN KEY (langId) REFERENCES Language(languageId);

ALTER TABLE MovieOverview
ADD FOREIGN KEY (filmId) REFERENCES Movie(apiid);

ALTER TABLE MoviesGenre
ADD FOREIGN KEY (apiId) REFERENCES Movie(apiid);

ALTER TABLE MoviesGenre
ADD FOREIGN KEY (genreId) REFERENCES Genre(genreId);

ALTER TABLE ProducersShow
ADD FOREIGN KEY (producerId) REFERENCES Producers(producerId);

ALTER TABLE ProducersShow
ADD FOREIGN KEY (showId) REFERENCES Shows(apiid);

ALTER TABLE ShowGenre
ADD FOREIGN KEY (apiId) REFERENCES Shows(apiid);

ALTER TABLE ShowGenre
ADD FOREIGN KEY (genreId) REFERENCES Genre(genreId);


ALTER TABLE ShowOverview
ADD FOREIGN KEY (showId) REFERENCES Shows(apiid);

ALTER TABLE PosterMovie
ADD FOREIGN KEY (apiId) REFERENCES Movie(apiid);

ALTER TABLE PosterShow
ADD FOREIGN KEY (apiId) REFERENCES Shows(apiid);
--====================================================================================================================--
-- 4) Adding indices
--====================================================================================================================--
ALTER TABLE Actors ADD INDEX id (actorId);
ALTER TABLE ActorsMovie ADD INDEX filmId (filmId);
ALTER TABLE ActorsShow ADD INDEX showId (showId);
ALTER TABLE DirectorsMovie ADD INDEX filmId (filmId);
ALTER TABLE Movie ADD INDEX langID (langId);
ALTER TABLE Movie ADD INDEX id (apiId);
ALTER TABLE Shows ADD INDEX langId (langId);
ALTER TABLE Shows ADD INDEX id (apiId);













