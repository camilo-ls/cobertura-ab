# Script de cálculo de Cobertura AB
### Desenvolvido no DCID/SEMSA - Manaus, AM

## O que é
O script foi desenvolvido para fazer, para a APS da cidade de Manaus, o cálculo de cobertura da atenção básica. Os parâmetros estão disponíveis nas Notas Metodológicas disponíveis [clicando aqui](https://egestorab.saude.gov.br/paginas/acessoPublico/relatorios/relHistoricoCoberturaAB.xhtml).

## Arquivos necessários
São necessárias os arquivos TXTLOCAL gerados pelos operadores do CNES. A pasta deve estar organizada da seguinte forma:

```
TXTLOCAL_COD-ESTADUAL/*.txt
TXTLOCAL_COD-MUNICIPAL/*.txt
pop.xlsx 
cnes.xlsx
```

- pop.xlsx
  - Planilha com os dados das populações por bairro/distrito/cidade.

- cnes.xlsx
  - Planilha com o RH dos funcionários da SEMSA

## Como executar
Com o python 3 instalado, execute no terminal:

> python script.py

A saída será uma planilha chamada cobertura.xlsx com as seguintes informações:
- Nome do bairro/distrito/cidade
- Quantidade de ESFs
- Quantidade de EAPs
- Quantidade de ESFs equivalentes
- Percentual da cobertura