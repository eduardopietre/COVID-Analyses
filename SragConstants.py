from enum import Enum

# File with constants
# Remember to use .value to compare things with enum values.

class CS_SEXO(Enum):  # opendatasus def is wrong. It is NOT 1, 2 and 9.
    MASCULINO = "M"
    FFMININO = "F"
    IGNORADO = "I"


class EVOLUCAO(Enum):
    CURA = 1
    OBITO = 2
    OUTRA_CAUSA = 3
    IGNORADO = 9


class CLASSI_FIN(Enum):
    INFLUENZA = 1
    OUTRO_VIRUS_RESP = 2
    OUTRO_AGENTE_ETIOLOGICO = 3
    NAO_ESPECIFICADO = 4
    COVID_19 = 5


class TP_IDADE(Enum):
    DIA = 1
    MES = 2
    ANOS = 3


# Columns that should be converted to INT.
CONVERT_TO_INT_COLUMNS = [
    "NU_IDADE_N",
    "TP_IDADE",
    "CLASSI_FIN",
    "EVOLUCAO",
]

SYMPTOMS_AND_COMORBIDITIES = [
	"FEBRE",
	"TOSSE",
	"GARGANTA",
	"DISPNEIA",
	"DESC_RESP",
	"SATURACAO",
	"DIARREIA",
	"VOMITO",
	"DOR_ABD",
    "FADIGA",
    "PERD_OLFT",
    "PERD_PALA",

    "PUERPERA",
	"CARDIOPATI",
	"HEMATOLOGI",
	"SIND_DOWN",
	"HEPATICA",
	"ASMA",
	"DIABETES",
	"NEUROLOGIC",
	"PNEUMOPATI",
	"IMUNODEPRE",
	"RENAL",
	"OBESIDADE",
	"OUT_MORBI",
]

# Colunas que queremos, descarta as demais
WANTED_COLUMNS = [
	"DT_NOTIFIC",
	"SG_UF_NOT",
	"CO_MUN_NOT",
	"CS_SEXO",
	"NU_IDADE_N",
	"TP_IDADE",
	"CS_GESTANT",
	"CS_RACA",
	"CS_ESCOL_N",

	"FEBRE",
	"TOSSE",
	"GARGANTA",
	"DISPNEIA",
	"DESC_RESP",
	"SATURACAO",
	"DIARREIA",
	"VOMITO",
	"DOR_ABD",
    "FADIGA",
    "PERD_OLFT",
    "PERD_PALA",

    "FATOR_RISC",
    "PUERPERA",
	"CARDIOPATI",
	"HEMATOLOGI",
	"SIND_DOWN",
	"HEPATICA",
	"ASMA",
	"DIABETES",
	"NEUROLOGIC",
	"PNEUMOPATI",
	"IMUNODEPRE",
	"RENAL",
	"OBESIDADE",
	"OBES_IMC",
	"OUT_MORBI",
	"MORB_DESC",

	# "HOSPITAL",
	"DT_INTERNA",
	"SUPORT_VEN",
	"RAIOX_RES",
    "TOMO_RES",
	# "PCR_OUTRO",
    "UTI",
    "SURTO_SG",
	"CLASSI_FIN",
	"EVOLUCAO",
    "DT_SIN_PRI",
	"DT_EVOLUCA",
	"DT_DIGITA",
]
