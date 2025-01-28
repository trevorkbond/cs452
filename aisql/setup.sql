create table ClothingSponsor (
    clothingSponsorId int primary key,
    sponsorName varchar(50) not null
);

create table RacketBrand (
    racketBrandId int primary key,
    brandName varchar(50) not null
);

create table Player (
    playerId int primary key,
    fullName varchar(50) not null,
    association char(3) not null,
    countryISO char(3) not null,
    careerWinnings bigint not null default 0,
    isActive boolean not null,
    constraint association_chk check (association in ('WTA', 'ATP'))
);

create table ClothingSponsorPlayer (
    clothingSponsorId int not null,
    playerId int not null,
    primary key (clothingSponsorId, playerId),
    foreign key (clothingSponsorId) references ClothingSponsor (clothingSponsorId),
    foreign key (playerId) references Player (playerId)
);

create table RacketBrandPlayer (
    racketBrandId int not null,
    playerId int not null,
    primary key (racketBrandId, playerId),
    foreign key (racketBrandId) references RacketBrand (racketBrandId),
    foreign key (playerId) references Player (playerId)
);

create table Tournament (
    tournamentId integer primary key,
    tournamentName varchar(50) not null,
    isGrandSlam boolean not null default 0,
    courtType varchar(10),
    constraint court_chk check (courtType in ('GRASS', 'HARD', 'CLAY'))
);

create table Match (
    winningPlayerId int not null,
    losingPlayerId int not null,
    score varchar(50) not null,
    tournamentId int not null,
    round varchar(5) not null,
    tournamentYear int not null,
    foreign key (winningPlayerId) references Player (playerId),
    foreign key (losingPlayerId) references Player (playerId),
    foreign key (tournamentId) references Tournament (tournamentId),
    constraint round_chk check (round in ('R1', 'R2', 'R3', 'R4', 'QF', 'SF', 'F'))
);
