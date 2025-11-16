
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

            
            SUM(
                CASE
                    WHEN UF = 'AL'
                        THEN 1
                    ELSE 0
                END
            ) AS Total_Proc_UF_AL,
            SUM(
                CASE
                    WHEN UF = 'AL'
                        AND ValorOcorrencia IS NOT NULL
                        AND ValorOcorrencia <> 0
                        THEN 1
                    ELSE 0
                END
            ) AS Total_Proc_com_valor_UF_AL,
            SUM(
                CASE
                    WHEN UF = 'AL'
                        THEN ValorOcorrencia
                    ELSE 0
                END
            ) AS Total_Valor_UF_AL,
            AVG(
                CASE
                    WHEN UF = 'AL'
                        THEN ValorOcorrencia
                END
            ) AS Media_Valor_UF_AL

        FROM base

        GROUP BY
            CPF_CNPJ,
            TipoPolo;
        
