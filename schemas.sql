create table if not exists welcome (
    guild_id bigint primary key,
    channel_id bigint not null,
    message varchar(255) not null default 'Welcome **{user}** to **{guild}**!'
);

-- create table if not exists user_levels(
--     user_id bigint not null primary key,
--     user_xp int not null default 0,
--     level int not null default 0
-- );

-- schemas.sql

-- Create the user_levels table if it doesn't exist
CREATE TABLE IF NOT EXISTS user_levels (
    user_id BIGINT NOT NULL PRIMARY KEY,
    user_xp INT NOT NULL DEFAULT 0,
    level INT NOT NULL DEFAULT 0
);
