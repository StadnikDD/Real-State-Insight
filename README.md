# **Real State Insight Project  - Seeking Opportunities in King County US-WA**

Projeto do tipo insight de um problema de negócio imobiliário fictício.

Para mais detalhes, acesse esse [dashboard](https://analytics-hrrs.herokuapp.com/)

## 1. **Questões do Negócio**

### 1. Sobre o negócio
House Rocket é uma empresa fictícia do setor imobiliário localizada em King County - Settle, WA - USA com seu modelo de negócio baseado na compra de imóveis com preços mais baixos em relação ao mercado, renovação e venda dos mesmo a fim de obter lucros . Um de seus desafios é encontrar bons negócios para compra dentro do portfólio disponível - Imóveis com boa localização, boas condições e alto potencial de lucros em sua revenda Desse modo, esse projeto tem objetivo de auxiliar o time de negócios a encontrar oportunidades que maximizem seus lucros e tornem a empresa mais rentável.

### 2. Qual a problema/dor/necessidade do time de negócio ?
   1. Não conseguem tomar boas decisões de compra sem analisar os dados.
   2. Portfólio muito grande, resultando em muito tempo para realizar o trabalho manualmente.

Desse modo, com um grande volume de dados a companhia gostaria de responder duas questões de negócio:
   1. **Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?**
   2. **Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?**

## 2. **Premissas de negócio.**

1. Para as condições de conservação da propriedade
   1. Se coluna 'condition' =< 2, então é condição ‘ruim’;
   2. Se coluna 'condition' = 3 OU 4, então é condição 'regular’;
   3. Se coluna 'condition' = 5, então é condição 'boa’.
2. Definição de compra
   1. Imóvel deve estar em boas ou intermediárias condições ( 'condition' ≥3);
   2. Ter vista para a água;
   3. Preço ser mais baixo que a mediana dos preços nas proximidades da propriedade, de modo que foi utilizado o código postal ('zipcode') como medida de proximidade.
3. Definição de venda
   1. Avaliação conforme sazonalidade (estações do ano);
   2. Definição da mediana dos preços nas proximidades da propriedade, utilizado o código postal ('zipcode') como medida de proximidade, e por sazonalidade;
   3. Para os imóveis definidos para compra:
      1. Venda do imóvel com 30% de ganho se o preço for menor que a mediana da região com os critérios definidos;
      2. Venda do imóvel com 10% de ganho se o preço for menor que a mediana da região com os critérios definidos.
4. ID duplicados são excluídos;
5. Conversão de pés para metros.

## 3. Planejamento da solução

1. Escopo do projeto:
   1. Resposta das perguntas de negocio;
   2. Validação das hipóteses;
   3. Entrega visualização/Dashboard no streamlit publicado no Heroku.
2. Ferramentas:
   1. Python;
   2. Jupyter Notebook;
   3. PyCharm;
   4. Streamlit;
   5. Heroku.
3. Processo
   1. Levantar dores e necessidades da empresa juntamente com hipóteses a serem validadas;
   2. Aquisição dos dados:
      1. Dados públicos no **[Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction?resource=download)**.
   3. Limpeza e transformação dos dados:
      1. Valores nulos;
      2. Tipos de dados;
      3. Duplicados;
      4. Outliers.
   4. Enginearing feature;
   5. Análise exploratória dos dados;
   6. Respondendo questões do negócio;
   7. Respondendo hipóteses;
   8. Estruturando visualização dos dados;
   9. Entendendo resultados e concluindo;
   10. Publicando na nuvem.

## 4. Insights dos dados

- H1: Imóveis que possuem vista para água, são 30% mais caros, na média;
  - VERDADEIRO - Imóveis com vista para a água são 212,42% mais caros, em média.
- H2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média;
  - FALSO - Imóveis construídos antes de 1955 são 0,62% mais baratos, em média.
- H3: Imóveis sem porão possuem área total (sqft_lot) 40% maior do que com porão;
  - FALSO - Imóveis com porão são 22,78% maiores, em média.
- H4: O crescimento do preço dos imóveis YoY ( Year over Year ) é de 10%;
  - FALSO - O aumento de preços YoY é 0,7%, em média.
- H5: Imóveis com 3 banheiros tem um crescimento MoM ( Month over Month ) de 15%;
  - FALSO - Nenhum crescimento MoM superou 15%.
- H6: Imóveis reformados a partir de 2000 são em média 60% mais caros que os renovados antes de 2000;
  - FALSO - O preço dos imóveis construídos depois de 200 é 15,9% mais caro que aqueles construídos antes de 2000.
- H7: Imóveis com restauração valem 30% ou mais que os sem restauração, em média;
  - VERDADEIRO - Em  média, o preço dos imóveis restaurados é 43,53% mais caro que os não renovados.
- H8: O preço de venda no verão é 50% maior que no inverno;
  - FALSO - O preço dos imóveis no verão é 5,19% mais caro que no inverno, em média.

## 5. Resultado financeiro para o negócio

10640 propriedades nas devidas condições fora consideradas para compra e venda. Sendo assim, haveria um custo de $4.200.241.289,0 para aquisição de todas as essas propriedades disponíveis com um potencial máximo de lucro de **$766.910.576,50**.

| Season | Maximum_profit |
| ------ | -------------- |
| Summer | 232,657,744.90 |
| Spring | 216,671,424.60 |
| Fall   | 189,545,236.60 |
| Winter | 128,036,170.40 |

No verão e primavera, os lucros máximos totais representam quase 59% do total juntos ($449.329.169,5).

## 6. Conclusão

Tendo como o objetivo principal deste projeto responder as seguintes questões:

1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço ?
2. Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço ?

Foi necessário realizar a coleta e limpeza dos dados para então dar início nas análises e testar algumas hipóteses. Para determinar as melhores oportunidades, os dados foram agrupados por localização, sazonalidade e se possuíam vista para a água ou não. Em seguida foram calculadas as medianas de preços nos agrupamentos para poder ser identificada as melhores oportunidades.

Com isso, foram identificadas 10.640 propriedades com bom potencial de negócio que possibilitam um lucro de até $766.910.576,50, sendo que as épocas mais propícias para maiores lucros são nos períodos mais quentes do ano.

## 8. Próximas etapas

Como se trata de um projeto inicial simples e sem complexidades, os próximos passos poderiam ser realizado com análises mais sofisticadas como:

- Analise estatística e aplicação de modelos de machine learning;
- Definição e validação de novas hipótese.

> Este projeto foi desenvolvido com suporte e sugestões da [Comunidade DS](https://www.comunidadedatascience.com/).
