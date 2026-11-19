# Predicción prenatal de la muerte fetal en MIMIC-IV

¿Se puede ver un riesgo alto de muerte fetal **antes** del ingreso para el parto, usando solo lo que se sabía de la mujer antes? Cuando la mujer llega al hospital, la muerte fetal muchas veces ya ocurrió; por eso este modelo usa solo información anterior al ingreso, de modo que el evento ocurre después de la información que lo predice. Sigue el framework por etapas para modelos de predicción clínica.

> **Estado (18/11/2026): auditoría de conteos hecha.** Ficha del desenlace escrita; se ejecutó la auditoría de la información disponible antes del ingreso (tarea A1). Siguiente: tabla de predictores.

[English version](README.md)

## Alcance

- **Desenlace:** muerte fetal identificada con los códigos CIE de la madre (definición estricta, 129 eventos en 19.440 hospitalizaciones de parto), siempre rotulada como proxy.
- **Punto de predicción:** hora de ingreso de la hospitalización de parto.
- **Información:** solo lo registrado al menos 7 días antes del ingreso (admisiones anteriores, mediciones ambulatorias, laboratorios ambulatorios) más atributos de la paciente (edad, raza y etnia, seguro, idioma, estado civil). Nada del ingreso actual.
- **Framework:** [`framework_es.md`](framework_es.md) (inglés: [`framework.md`](framework.md)), versión 1.0. Ficha del desenlace: [`docs/outcome_card_antenatal_es.md`](docs/outcome_card_antenatal_es.md) (inglés: [`docs/outcome_card_antenatal.md`](docs/outcome_card_antenatal.md)).

La auditoría de conteos de la información disponible antes del ingreso (ejecutada el 18/11/2026) está redactada en [`count_audit_es.md`](count_audit_es.md) (inglés: [`count_audit.md`](count_audit.md)): cada consulta, qué mostró y qué significa para los predictores.

## Requisitos y orden de ejecución

Una base local de PostgreSQL con MIMIC-IV v3.1 (módulo hosp). Todas las tablas del modelo se construyen desde este repositorio, con nombres que empiezan por `antenatal_`, de modo que no se modifica ninguna otra tabla de la base. Cada script se ejecuta completo en una sola conexión (DBeaver: Alt+X), en este orden:

| Orden | Script | Crea | Etapa del framework |
|---|---|---|---|
| 1 | `sql/00_cohort_and_label/01_obstetric_universe_es.sql` | `antenatal_obstetric_universe` (universo obstétrico, marca de parto) | E2 |
| 2 | `sql/00_cohort_and_label/02_fetal_death_label_es.sql` | `antenatal_fetal_death_codes`, `antenatal_fetal_death_label` (etiqueta por admisión) | E3, P1 |
| 3 | `sql/01_audit_counts/01_prior_information_es.sql` | Nada (solo lectura): auditoría de conteos | E4 |
| 4 | `sql/02_predictors/01_predictor_table_es.sql` | `antenatal_predictors_v1` (tabla de predictores, la que leen los modelos) | E6, E7 |

Conteos de referencia que deben reproducirse: 25.736 admisiones obstétricas; 19.440 admisiones en la población del modelo, de 13.735 pacientes; 129 eventos estrictos y 142 con códigos parciales.

## Estructura del repositorio

```
sql/00_cohort_and_label/ Universo obstétrico, marca de parto, catálogo de códigos y etiqueta de muerte fetal
sql/01_audit_counts/   Conteos de la información disponible antes del ingreso (solo lectura, salida agregada)
sql/02_predictors/     Tabla de predictores de la ventana de información
notebooks/             Modelos, validación y clasificación
libraries/             Conexión a la base (variables de entorno) y utilidades
scripts/               check_sql_pair.py: cada script SQL y su versión _es deben tener el mismo código
data/                  Solo salidas agregadas outputs_*.txt (conteos y métricas)
docs/                  Ficha del desenlace, figura del framework, documentos de reporte
```

Cada script SQL tiene una versión en español con el sufijo `_es` y el mismo código. Solo se publican salidas agregadas; ningún `subject_id`, `hadm_id` ni fila a nivel de paciente, y los conteos menores de 5 se muestran como "<5".

## Acceso a los datos

MIMIC-IV está disponible para usuarios acreditados en PhysioNet bajo su acuerdo de uso de datos. Copie `.env.example` a `.env` con sus credenciales locales; `.env` nunca se versiona.

*Confidencial: uso interno del proyecto de investigación.*
