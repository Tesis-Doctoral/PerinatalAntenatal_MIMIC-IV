# Ficha del desenlace — predicción prenatal de la muerte fetal, MIMIC-IV

Versión 2, 18/11/2026 (versión 1 del mismo día, actualizada con la auditoría de conteos A1: [`../count_audit_es.md`](../count_audit_es.md)). Tercera aplicación del framework por etapas ([`../framework_es.md`](../framework_es.md), versión 1.0). Es el retorno **R3** (otro punto de predicción) del desenlace *muerte perinatal antes del nacimiento*, cuyo primer modelo (`PerinatalMortality_MIMIC-IV`, predicción a las 6 h del ingreso) encontró que 73 de 129 muertes fetales ya estaban presentes en el punto de predicción (auditoría de conteos, grupo G, tarea T45). Los campos marcados **pendiente** se fijan, y se registran en el libro de decisiones, antes de la puerta que los necesita. Versión en inglés: [`outcome_card_antenatal.md`](outcome_card_antenatal.md).

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
| Por qué 7 días | Una muerte fetal diagnosticada en una consulta ambulatoria suele seguirse de un ingreso en pocos días. El margen deja fuera del modelo la información registrada después de la muerte. Sensibilidad: 1 y 30 días (la auditoría solo perdió 3 eventos con información entre ellos) |
| Ventana del embarazo actual | Las mediciones y los laboratorios del embarazo actual se toman **entre 280 y 7 días antes** del ingreso (aproximadamente un embarazo). No se usan valores anteriores; si no hay valor en esta ventana, el predictor queda faltante, con su indicador |
| También permitido | Atributos de la paciente en el ingreso actual que no dependen de cómo llegó: edad, raza y etnia, seguro, idioma, estado civil |
| Excluido | Todo lo del ingreso actual: diagnósticos, procedimientos, laboratorios, tipo y lugar de admisión (reflejan cómo se presentó, algo que el propio evento puede causar), datos de urgencias |

## 4. Predictores (E7), fijados con la auditoría de conteos

Fijados el 18/11/2026 con las frecuencias de la auditoría de conteos (toda la población, nunca separada por desenlace) y razones clínicas. **Que no haya registro no significa que no exista la condición**: muchas mujeres no tienen atenciones anteriores en este hospital, por eso los bloques llevan indicadores.

| Bloque | Predictores | Parámetros | Fuente en la auditoría |
|---|---|---|---|
| Registro | Edad (continua); raza y etnia (blanca, negra, hispana, asiática, otra o desconocida); seguro (Medicaid, privado, Medicare u otro o faltante); idioma (inglés, otro o faltante); estado civil (casada, no casada, faltante) | 10 | Q-A7 |
| Historia de atenciones | Alguna admisión anterior; admisión en los 90 días previos (embarazo actual) | 2 | Q-A1, Q-A3 |
| Antecedentes (admisiones anteriores) | Cesárea anterior; trastorno hipertensivo en embarazo anterior; hipertensión crónica; diabetes pregestacional; diabetes gestacional en embarazo anterior; consumo de tabaco, alcohol o drogas; enfermedad tiroidea; **resultado adverso en embarazo anterior** (muerte fetal o parto pretérmino); **otra condición crónica de alto riesgo** (lupus, antifosfolípido o trombofilia; VIH o sífilis; enfermedad renal crónica) | 9 | Q-A4 |
| Controles del embarazo actual (omr) | Última presión sistólica y última diastólica; alguna presión de 140/90 o más; último índice de masa corporal (si falta, calculado con el último peso y cualquier talla) | 4 | Q-A5 |
| Laboratorio del embarazo actual | Última hemoglobina | 1 | Q-A6 |
| Indicador | Tuvo control prenatal en este hospital (alguna medición o laboratorio ambulatorio en la ventana del embarazo actual) | 1 | Q-A1, Q-A5, Q-A6 |
| **Total** | | **27** | |

**Descartados, con su razón:** número de admisiones anteriores y días desde el último egreso (reemplazados por el indicador de 90 días); obesidad por código (el índice de masa corporal medido es más preciso y tiene mucha más cobertura); creatinina (valores antiguos, poca información; la enfermedad renal está en el compuesto); hemoglobina glicosilada (se pide de forma selectiva; la diabetes está cubierta por los antecedentes); condiciones raras como predictores sueltos (unidas en los dos compuestos).

**Límites de plausibilidad:** sistólica 60–250 mmHg, diastólica 30–150 mmHg, índice de masa corporal 12–80 kg/m², peso 70–600 lb, talla 48–84 pulgadas, hemoglobina 3–20 g/dL. Los valores por fuera quedan faltantes.

## 5. Tamaño de muestra y modelo (P3, E8)

| Campo | Valor |
|---|---|
| Parámetros candidatos | 27 |
| Parámetros soportados | Entre 17 y 25, según la estimación previa del perinatal (mismos eventos y prevalencia); la puerta usa el R² de Cox-Snell observado |
| Modelo principal | Regresión logística penalizada (menos de 20 eventos por parámetro); modelos de árboles y ensamble como comparaciones |
| Conjunto reducido (17 parámetros) | Edad; raza y etnia (4); Medicaid; inglés; casada; tuvo control prenatal en este hospital; última sistólica; presión elevada; índice de masa corporal; hemoglobina; antecedente hipertensivo (crónico o en embarazo anterior); diabetes (pregestacional o gestacional en embarazo anterior); resultado adverso en embarazo anterior. Fijado el 18/11/2026, antes de cualquier modelo; nunca elegido por asociación con el desenlace |

## 5b. Análisis de sensibilidad

| Análisis | Pregunta |
|---|---|
| Márgenes de 1 y 30 días | ¿El resultado depende del margen? |
| Solo pacientes con alguna información previa (99 eventos) | ¿El resultado depende de quién tiene historia en este hospital? |
| Calibración por período | ¿El modelo funciona igual en períodos con menos historia (C4; la auditoría encontró menos información en los períodos recientes)? |
| Estricta más parcial; 22 y 28 semanas o más; sin códigos de pérdida temprana | ¿Las definiciones de la etiqueta cambian el resultado? (D5 perinatal) |

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

1. ~~Auditoría de conteos A1~~ (hecha el 18/11/2026, [`../count_audit_es.md`](../count_audit_es.md)).
2. Tabla de predictores: `sql/02_predictors/01_predictor_table_es.sql` (tarea A2), una fila por admisión y margen.
3. Verificación del tamaño de muestra con el R² de Cox-Snell observado (P3); conjunto reducido si hace falta.
4. Validación anidada agrupada, criterios C1, C2 y C4, clasificación.

*Confidencial: uso interno del proyecto de investigación.*
