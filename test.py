import pandas as pd

from classes.databse_communications import DBComms
db_comms = DBComms()
db_comms.conn_open()


class SendQuery(object):

    def __init__(self):
        pass

    def count_processos_estado(
        self,
        valor_documento,
        data
    ):

        query_slices = []

        list_estados = [
            "AL", #"CE", "PB", "PE", "BA", "MA",
            # "SE", "PI", "RN", "AC", "AM", "AP",
            # "RR", "RO", "PA", "RJ", "DF", "ES",
            # "GO", "MG", "PR", "SC", "SP", "TO",
            # "RS", "MT", "MS"
        ]

        for estado in list_estados:

            block_columns = f"""
            SUM(
                CASE
                    WHEN UF = '{estado}'
                        THEN 1
                    ELSE 0
                END
            ) AS Total_Proc_UF_{estado},
            SUM(
                CASE
                    WHEN UF = '{estado}'
                        AND ValorOcorrencia IS NOT NULL
                        AND ValorOcorrencia <> 0
                        THEN 1
                    ELSE 0
                END
            ) AS Total_Proc_com_valor_UF_{estado},
            SUM(
                CASE
                    WHEN UF = '{estado}'
                        THEN ValorOcorrencia
                    ELSE 0
                END
            ) AS Total_Valor_UF_{estado},
            AVG(
                CASE
                    WHEN UF = '{estado}'
                        THEN ValorOcorrencia
                END
            ) AS Media_Valor_UF_{estado}"""
            query_slices.append(block_columns)

        block_estados = ",\n".join(query_slices)

        query = f"""
        WITH base AS (
        SELECT
            pa.CPF_CNPJ,
            pa.TipoPolo,
            pa.UF,
            pr.NumeracaoProcessualUnica,
            pr.ValorOcorrencia,
            pr.DataDistribuicao
        FROM KurierPartesAtribuidas.dbo.PartesAtribuidas AS pa
        INNER JOIN KurierTribunal2.dbo.Processo AS pr
            ON pr.NumeracaoProcessualUnica = pa.NPU
        WHERE
            pa.CPF_CNPJ = ?
            AND pa.TipoPolo IN ('Autor', 'Reu')
        )

        SELECT

            {block_estados}

        FROM base

        GROUP BY
            CPF_CNPJ,
            TipoPolo;
        """

        # tabela_processos = pd.read_sql_query(
        #     query,
        #     db_comms.conn,
        #     params=[
        #         valor_documento,
        #         data
        #     ]
        # )

        # return tabela_processos

        return query

send_query = SendQuery()

q = send_query.count_processos_estado('123123123', '123123')
