CREATE TABLE IF NOT EXISTS "user" (
    -- Account fields
    username TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    coins INTEGER NOT NULL DEFAULT 500,

    -- Profile fields (phone_number and country optional - for "verify later")
    full_name TEXT,
    phone_number TEXT,  -- Optional - can be provided later for verification
    birth_date DATE NOT NULL,  -- Required for age validation
    country TEXT,  -- Optional - can be provided later for verification

    -- Legal/compliance fields
    accepted_terms BOOLEAN NOT NULL DEFAULT FALSE,
    accepted_privacy_policy BOOLEAN NOT NULL DEFAULT FALSE,
    is_adult BOOLEAN NOT NULL,
    verified_at TIMESTAMP,  -- NULL = identity verification pending

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT user_coins_non_negative CHECK (coins >= 0),
    CONSTRAINT user_must_be_adult CHECK (is_adult = TRUE),
    CONSTRAINT user_must_accept_terms CHECK (accepted_terms = TRUE),
    CONSTRAINT user_must_accept_privacy CHECK (accepted_privacy_policy = TRUE)
);

CREATE TABLE IF NOT EXISTS bet (
    id UUID PRIMARY KEY,
    user_id TEXT NOT NULL,                 -- creator username
    cost NUMERIC NOT NULL DEFAULT 0,       -- entry fee
    amount NUMERIC NOT NULL DEFAULT 0,     -- ✅ pot acumulat
    status TEXT NOT NULL DEFAULT 'open',
    name TEXT NOT NULL,
    create_date TIMESTAMP NOT NULL,
    update_date TIMESTAMP NOT NULL,

    CONSTRAINT bet_cost_non_negative CHECK (cost >= 0),
    CONSTRAINT bet_amount_non_negative CHECK (amount >= 0),

    CONSTRAINT fk_bet_user
        FOREIGN KEY (user_id) REFERENCES "user"(username)
        ON DELETE CASCADE
);



-- Taula de grups
CREATE TABLE IF NOT EXISTS "group" (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    admin_username TEXT NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT NOW(),
    update_date TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_group_admin
        FOREIGN KEY (admin_username) REFERENCES "user"(username)
        ON DELETE CASCADE
);

-- Relació molts-a-molts: usuaris <-> grups
CREATE TABLE IF NOT EXISTS group_member (
    group_id UUID NOT NULL,
    username TEXT NOT NULL,
    join_date TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (group_id, username),
    CONSTRAINT fk_member_group
        FOREIGN KEY (group_id) REFERENCES "group"(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_member_user
        FOREIGN KEY (username) REFERENCES "user"(username)
        ON DELETE CASCADE
);

-- Relació grups <-> bets
CREATE TABLE IF NOT EXISTS group_bet (
    group_id UUID NOT NULL,
    bet_id UUID NOT NULL,
    create_date TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (group_id, bet_id),
    CONSTRAINT fk_group_bet_group
        FOREIGN KEY (group_id) REFERENCES "group"(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_group_bet_bet
        FOREIGN KEY (bet_id) REFERENCES bet(id)
        ON DELETE CASCADE
);

-- ✅ Participants d'una bet (usuaris que s'hi uneixen)
CREATE TABLE IF NOT EXISTS bet_participant (
    bet_id UUID NOT NULL,
    username TEXT NOT NULL,
    join_date TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (bet_id, username),
    CONSTRAINT fk_bp_bet
        FOREIGN KEY (bet_id) REFERENCES bet(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_bp_user
        FOREIGN KEY (username) REFERENCES "user"(username)
        ON DELETE CASCADE
);
