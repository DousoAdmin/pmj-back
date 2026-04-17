-- Cambios solicitados: quitar lastname y crear tipo de documento de persona

-- 1) Crear tabla typedocumentspersons
CREATE TABLE IF NOT EXISTS typedocumentspersons (
    TPDU_PK INT PRIMARY KEY AUTO_INCREMENT,
    TPDU_name VARCHAR(50) NOT NULL,
    TPDU_code VARCHAR(10) NOT NULL,
    TPDU_description VARCHAR(255),
    TPDU_date_create DATE,
    TPDU_user_create INT
);

-- 2) Agregar FK en persons hacia typedocumentspersons
ALTER TABLE persons
ADD COLUMN IF NOT EXISTS PRSN_FK_typedocumentspersons INT NULL,
ADD CONSTRAINT fk_persons_typedocumentspersons
FOREIGN KEY (PRSN_FK_typedocumentspersons)
REFERENCES typedocumentspersons(TPDU_PK);

-- 3) Eliminar columna lastname (solo si existe)
ALTER TABLE persons
DROP COLUMN IF EXISTS PRSN_lastname;
