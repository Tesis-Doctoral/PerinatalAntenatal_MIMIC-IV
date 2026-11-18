# Ficha del desenlace — predicción prenatal de la muerte fetal, MIMIC-IV

Versión 1, 18/11/2026. Tercera aplicación del framework por etapas ([`../framework_es.md`](../framework_es.md), versión 1.0). Es el retorno **R3** (otro punto de predicción) del desenlace *muerte perinatal antes del nacimiento*, cuyo primer modelo (`PerinatalMortality_MIMIC-IV`, predicción a las 6 h del ingreso) encontró que 73 de 129 muertes fetales ya estaban presentes en el punto de predicción (auditoría de conteos, grupo G, tarea T45). Los campos marcados **pendiente** se fijan, y se registran en el libro de decisiones, antes de la puerta que los necesita. Versión en inglés: [`outcome_card_antenatal.md`](outcome_card_antenatal.md).

## 1. La pregunta

Al ingreso, la muerte fetal muchas veces ya ocurrió: un modelo a las 6 h del ingreso la reconoce (identificador temprano). Este modelo hace otra pregunta: **con lo que se sabía de la mujer antes de este ingreso, ¿se podía ver un riesgo alto de muerte fetal?** Solo entra información registrada antes del ingreso, así que el evento ocurre después de la información que lo predice.

## 2. Identidad

| Campo | Valor | Fuente |
|---|---|---|
| Desenlace | Muerte perinatal antes del nacimiento (muerte fetal o mortinato), siempre rotulada como proxy | D2 perinatal |
| Peldaño | Mismo desenlace; nuevo punto de predicción (retorno R3) | — |
| Fuente de datos | MIMIC-IV v3.1; tablas de los proyectos materno y perinatal (sección 7) | — |
| Unidad y grupo | Hospitalización de parto; paciente como unidad de agrupación | D4 perinatal |
| Población | Población de la D3 perinatal: bandera de parto (v2) o código de mortinato, 19.440 admisiones | D3 perinatal |
| Etiqueta principal | Código estricto a cualquier edad gestacional (`fetal_death_label_v2.label_main`): 129 eventos (0,66%) | D5 perinatal, T16 |
| Etiquetas de sensibilidad | Estricta más parcial; 22 y 28 semanas o más (solo CIE-10); sin códigos de pérdida temprana | D5 perinatal |

## 3. Punto de predicción y ventana de información (E6)

| Campo | Valor |
|---|---|
| Tiempo cero y punto de predicción | Hora de ingreso de la hospitalización de parto |
| Ventana de información | Todo lo registrado **al menos 7 días antes** del ingreso: admisiones anteriores de MIMIC-IV con egreso hasta entonces, mediciones ambulatorias (OMR) y laboratorios ambulatorios fechados hasta entonces |
| Por qué 7 días | Una muerte fetal diagnosticada en una consulta ambulatoria suele seguirse de un ingreso en pocos días. El margen deja fuera del modelo la información registrada después de la muerte. Sensibilidad: 1 y 30 días |
| También permitido | Atributos de la paciente en el ingreso actual que no dependen de cómo llegó: edad, raza y etnia, seguro, idioma, estado civil |
| Excluido | Todo lo del ingreso actual: diagnósticos, procedimientos, laboratorios, tipo y lugar de admisión (reflejan cómo se presentó, algo que el propio evento puede causar), datos de urgencias |

## 4. Predictores candidatos (E7)

Elegidos por razón clínica antes de cualquier modelo; la lista final depende de la cobertura (conteos de la sección 8, regla de cobertura del 10% de la población). Cada bloque tiene un indicador de si existe información: **que no haya registro no significa que no exista la condición**, porque muchas mujeres no tienen atenciones anteriores en este hospital.

| Bloque | Variables |
|---|---|
| Registro | Edad; raza y etnia (5 grupos); seguro; idioma; estado civil |
| Historia de atenciones | Alguna admisión anterior; número de admisiones anteriores; alguna admisión obstétrica anterior; días desde el último egreso |
| Antecedentes obstétricos (admisiones anteriores) | Muerte fetal o mortinato anterior; parto pretérmino anterior; cesárea anterior; preeclampsia, eclampsia o hipertensión gestacional anterior; diabetes gestacional en un embarazo anterior |
| Condiciones crónicas (admisiones anteriores) | Hipertensión crónica; diabetes pregestacional; obesidad; enfermedad renal crónica; enfermedad tiroidea; lupus o síndrome antifosfolípido; trombofilia; consumo de tabaco, alcohol o drogas; VIH o sífilis |
| Mediciones ambulatorias (OMR) | Último índice de masa corporal, peso, presión sistólica y diastólica en la ventana |
| Laboratorios ambulatorios | Última hemoglobina glicosilada, hemoglobina y creatinina en la ventana |

## 5. Tamaño de muestra y modelo (P3, E8)

| Campo | Valor |
|---|---|
| Parámetros candidatos | **Pendiente** (contar cada categoría e indicador) |
| Parámetros soportados | Entre 17 y 25, según la estimación previa del perinatal (mismos eventos y prevalencia); la puerta usa el R² de Cox-Snell observado |
| Modelo principal | Regresión logística penalizada (menos de 20 eventos por parámetro); modelos de árboles y ensamble como comparaciones |
| Conjunto reducido | Se fija antes de P3: registro, indicador de historia de atenciones, las tres variables de antecedentes obstétricos con más cobertura, hipertensión crónica, diabetes pregestacional, última presión arterial e índice de masa corporal con sus indicadores. Nunca se elige por asociación con el desenlace |

## 6. Criterios de clasificación (P4)

| Criterio | Cómo se aplica | Estado |
|---|---|---|
| C1, eventos ya presentes | La ventana de información cierra 7 días antes del ingreso, así que una muerte posterior a ese momento ocurre después de la información. Una muerte anterior no puede descartarse con códigos; los márgenes de 1 y 30 días miden cuánto importa | Aplica mediante la sensibilidad del margen |
| C2, desenlace con tiempo | El evento es posterior a la ventana de información por diseño | Aplica |
| C3, sesgo de detección | El desenlace no se define con un examen | No aplica |
| C4, estabilidad en el tiempo | Desarrollo antes de 2017 y una sola prueba de 2017 en adelante | Aplica |

**Dicho antes de los resultados.** Los modelos prenatales de mortinato basados en características maternas suelen alcanzar una AUROC de 0,60 a 0,75. El framework clasifica un modelo como predictor solo con AUROC de 0,75 o más, así que este modelo podría quedar como *ninguno* si queda por debajo. El umbral no se cambia para este desenlace; cualquier propuesta de cambio debe decidirse con el director antes de ajustar el primer modelo.

## 7. Requisitos (construidos por los otros proyectos)

`mimiciv.cohort_obstetric_v2`, `mimiciv.hadm_delivery_v2` (MaternalMortality_MIMIC-IV_Cureus) y `mimiciv.fetal_death_label_v2` (PerinatalMortality_MIMIC-IV, tarea T16), más las tablas de MIMIC-IV `admissions`, `patients`, `diagnoses_icd`, `omr`, `labevents`.

## 8. Próximas tareas

1. Auditoría de conteos A1: cuántas admisiones de la población tienen información en la ventana (admisión anterior, OMR, laboratorio ambulatorio), en eventos y no eventos, por era y por margen.
2. Cobertura de cada predictor candidato; fijar la lista final y los parámetros candidatos.
3. Tabla de predictores; verificación del tamaño de muestra (P3).
4. Validación anidada agrupada, criterios C1, C2 y C4, clasificación.

*Confidencial: uso interno del proyecto de investigación.*
