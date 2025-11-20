CREATE TABLE padron_tse (
    cedula            CHAR(9) PRIMARY KEY,
    nombre            VARCHAR(50),
    apellido1         VARCHAR(50),
    apellido2         VARCHAR(50)
);

CREATE TABLE usuarios (
    id_usuario       SERIAL PRIMARY KEY,
    cedula           CHAR(9) NOT NULL UNIQUE,
    nombre           VARCHAR(50) NOT NULL,
    apellido1        VARCHAR(50) NOT NULL,
    apellido2        VARCHAR(50),
    correo           VARCHAR(150) NOT NULL UNIQUE,
    hash_contrasena  TEXT NOT NULL,
    rol              VARCHAR(20) NOT NULL,  -- 'votante', 'administrador', 'candidato'
    esta_activo      BOOLEAN DEFAULT TRUE,
    fecha_creacion   TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_usuarios_padron
      FOREIGN KEY (cedula) REFERENCES padron_tse(cedula),

    CONSTRAINT chk_usuarios_rol
      CHECK (rol IN ('votante', 'administrador', 'candidato'))
);

CREATE TABLE elecciones (
    id_eleccion      SERIAL PRIMARY KEY,
    
    nombre_eleccion  VARCHAR(200) NOT NULL,
    descripcion      TEXT,
    
    fecha_inicio     TIMESTAMP NOT NULL,
    fecha_fin        TIMESTAMP NOT NULL,
    
    estado           VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    
    fecha_creacion   TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT chk_elecciones_estado
      CHECK (estado IN ('pendiente', 'activa', 'cerrada')),
    
    CONSTRAINT chk_elecciones_fechas
      CHECK (fecha_fin > fecha_inicio)
);

CREATE TABLE candidatos (
    id_candidato   SERIAL PRIMARY KEY,

    id_eleccion    INTEGER NOT NULL,
    id_usuario     INTEGER NOT NULL,

    propuesta      VARCHAR(500),  -- Texto corto con su plan/idea

    fecha_registro TIMESTAMP DEFAULT NOW(),

    -- Relaciones
    CONSTRAINT fk_candidato_eleccion
        FOREIGN KEY (id_eleccion)
        REFERENCES elecciones(id_eleccion)
        ON DELETE CASCADE,

    CONSTRAINT fk_candidato_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    -- Un usuario no puede ser candidato dos veces en la misma elección
    CONSTRAINT unq_candidato_eleccion_usuario
        UNIQUE (id_eleccion, id_usuario)
);

CREATE TABLE votos (
    id_voto         SERIAL PRIMARY KEY,

    id_eleccion     INTEGER NOT NULL,
    id_usuario      INTEGER NOT NULL,   -- solo para validar que ya votó

    voto_cifrado    TEXT NOT NULL,      -- ciphertext con Paillier
    hash_blockchain TEXT NOT NULL,      -- ID / hash de la transacción en blockchain

    fecha_voto      TIMESTAMP DEFAULT NOW(),

    -- Relaciones
    CONSTRAINT fk_voto_eleccion
        FOREIGN KEY (id_eleccion)
        REFERENCES elecciones(id_eleccion)
        ON DELETE CASCADE,

    CONSTRAINT fk_voto_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE,

    -- Evitar doble voto por elección
    CONSTRAINT unq_voto_eleccion_usuario
        UNIQUE (id_eleccion, id_usuario)
);

CREATE TABLE resultados (
    id_eleccion       INTEGER NOT NULL,
    id_candidato      INTEGER NOT NULL,

    resultado_cifrado TEXT NOT NULL,   -- E(total) = suma homomórfica de los votos
    hash_blockchain   TEXT,            -- hash/txid de verificación en cadena

    fecha_calculo     TIMESTAMP DEFAULT NOW(),

    -- PK compuesta
    PRIMARY KEY (id_eleccion, id_candidato),

    -- Relaciones
    CONSTRAINT fk_res_eleccion
        FOREIGN KEY (id_eleccion)
        REFERENCES elecciones(id_eleccion)
        ON DELETE CASCADE,

    CONSTRAINT fk_res_candidato
        FOREIGN KEY (id_candidato)
        REFERENCES candidatos(id_candidato)
        ON DELETE CASCADE
);

CREATE TABLE logs_auditoria (
    id_log          SERIAL PRIMARY KEY,

    id_usuario      INTEGER,               -- Puede ser NULL para logs del sistema
    fecha_hora      TIMESTAMP DEFAULT NOW(),

    accion          VARCHAR(50) NOT NULL,  -- LOGIN, VOTO_EMITIDO, CREAR_ELECCION, ERROR, etc.
    detalles        TEXT,                  -- Información adicional según la acción
    hash_blockchain TEXT,                  -- Hash opcional para anclaje en cadena

    -- Relación (puede ser NULL en acciones sin usuario)
    CONSTRAINT fk_log_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL,

    -- Validación del tipo de acción
    CONSTRAINT chk_log_accion
        CHECK (accion IN (
            'LOGIN', 
            'LOGOUT',
            'VOTO_EMITIDO',
            'CREAR_ELECCION',
            'CERRAR_ELECCION',
            'CREAR_CANDIDATO',
            'ERROR',
            'SISTEMA'
        ))
);
