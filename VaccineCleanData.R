

# This script may take a long time to run
# it expects "data/vacina_parcial {date}.csv" and cleans it to reduce size.
# This csv file must be downloaded from https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao
# and should be renamed.
# data will be exported to "data/vacine_data_subset {date}.rda", df object named 'vacine_data_subset'.


date_str = "25-02-21"

data <-read.csv(paste0("data/vacina_parcial ", date_str, ".csv"), encoding="UTF-8")
vacine_data_subset <- subset(data, select=c(
    "paciente_idade",
    "paciente_dataNascimento",
    "paciente_enumSexoBiologico",
    "paciente_racaCor_valor",
    "paciente_endereco_nmMunicipio",
    "paciente_endereco_uf",
    "estabelecimento_razaoSocial",
    "estalecimento_noFantasia",
    "estabelecimento_municipio_nome",
    "estabelecimento_uf",
    "vacina_grupoAtendimento_nome",
    "vacina_categoria_nome",
    "vacina_dataAplicacao",
    "vacina_descricao_dose",
    "vacina_nome",
    "sistema_origem"
))

to_factor = c(
    "paciente_enumSexoBiologico",
    "paciente_racaCor_valor",
    "paciente_endereco_nmMunicipio",
    "paciente_endereco_uf",
    "estabelecimento_municipio_nome",
    "estabelecimento_uf",
    "vacina_grupoAtendimento_nome",
    "vacina_categoria_nome",
    "vacina_descricao_dose",
    "vacina_nome",
    "sistema_origem"
)

vacine_data_subset[to_factor] <- lapply(vacine_data_subset[to_factor], as.factor)

save(vacine_data_subset, file=paste0("data/vacine_data_subset ", date_str, ".rda"))
