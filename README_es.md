# Predicción prenatal de la muerte fetal en MIMIC-IV

¿Se puede ver un riesgo alto de muerte fetal **antes** del ingreso para el parto, usando solo lo que se sabía de la mujer antes? Este proyecto es el modelo prenatal del desenlace de la tesis *muerte perinatal antes del nacimiento*. Es el retorno R3 (otro punto de predicción) del framework por etapas, abierto porque el modelo a las 6 h del ingreso (`PerinatalMortality_MIMIC-IV`) encontró que la mayoría de las muertes fetales ya estaban presentes en su punto de predicción.

> **Estado (18/11/2026): auditoría de conteos hecha.** Ficha del desenlace escrita; se ejecutó la auditoría de la información disponible antes del ingreso (tarea A1). Siguiente: tabla de predictores.

[English version](README.md)

## Alcance

- **Desenlace:** muerte fetal identificada con los códigos CIE de la madre (definición estricta, 129 eventos en 19.440 hospitalizaciones de parto), siempre rotulada como proxy. Misma etiqueta que `PerinatalMortality_MIMIC-IV`.
- **Punto de predicción:** hora de ingreso de la hospitalización de parto.
- **Información:** solo lo registrado al menos 7 días antes del ingreso (admisiones anteriores, mediciones ambulatorias, laboratorios ambulatorios) más atributos de la paciente (edad, raza y etnia, seguro, idioma, estado civil). Nada del ingreso actual.
- **Framework:** [`framework_es.md`](framework_es.md) (inglés: [`framework.md`](framework.md)), versión 1.0. Ficha del desenlace: [`docs/outcome_card_antenatal_es.md`](docs/outcome_card_antenatal_es.md) (inglés: [`docs/outcome_card_antenatal.md`](docs/outcome_card_antenatal.md)).

La auditoría de conteos de la información disponible antes del ingreso (ejecutada el 18/11/2026) está redactada en [`count_audit_es.md`](count_audit_es.md) (inglés: [`count_audit.md`](count_audit.md)): cada consulta, qué mostró y qué significa para los predictores.

## Requisitos

La cohorte y la etiqueta las construyen los proyectos compañeros y se leen de la misma base local de MIMIC-IV:

| Tabla | Construida por |
|---|---|
| `mimiciv.cohort_obstetric_v2`, `mimiciv.hadm_delivery_v2` | `MaternalMortality_MIMIC-IV_Cureus` |
| `mimiciv.fetal_death_label_v2` | `PerinatalMortality_MIMIC-IV` (tarea T16) |

## Estructura del repositorio

```
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
