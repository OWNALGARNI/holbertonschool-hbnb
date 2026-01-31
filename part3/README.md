Diagram

    USERS {
        VARCHAR id PK
        VARCHAR email
        VARCHAR password
        VARCHAR first_name
        VARCHAR last_name
        BOOLEAN is_admin
        DATETIME created_at
        DATETIME updated_at
    }

    PLACES {
        VARCHAR id PK
        VARCHAR title
        VARCHAR description
        INT price
        FLOAT latitude
        FLOAT longitude
        VARCHAR owner_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    REVIEWS {
        VARCHAR id PK
        VARCHAR text
        INT rating
        VARCHAR place_id FK
        VARCHAR user_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    AMENITIES {
        VARCHAR id PK
        VARCHAR name
        DATETIME created_at
        DATETIME updated_at
    }

    PLACE_AMENITY {
        VARCHAR place_id PK, FK
        VARCHAR amenity_id PK, FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : has
    PLACES ||--o{ PLACE_AMENITY : links
    AMENITIES ||--o{ PLACE_AMENITY : links
