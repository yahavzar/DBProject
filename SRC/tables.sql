
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
);

create TABLE IF NOT EXISTS LanguageMovie(
languageId int,
movieId int
);

create TABLE IF NOT EXISTS Directors(
directorId int PRIMARY KEY,
directorName varchar(32)
);

create TABLE IF NOT EXISTS ActorsMovie(
actorId int,
filmId int
);

create TABLE IF NOT EXISTS DirectorsMovie(
directorId int,
filmId int
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
);

create TABLE IF NOT EXISTS LanguageShow(
languageId int,
showId int
);

create TABLE IF NOT EXISTS Producers(
producerId int PRIMARY KEY,
producerName varchar(32)
);

create TABLE IF NOT EXISTS ActorsShow(
actorId int,
showId int
);

create TABLE IF NOT EXISTS ProducersShow(
producerId int,
showId int
);

create TABLE IF NOT EXISTS ShowOverview(
showId int PRIMARY KEY,
overview varchar(2048)
);
