# necessario instalar

# install.packages('FactoMineR')
# install.packages('factoextra')
# install.packages('pollster')
# install.packages('dplyr')
# install.packages('knitr')
# install.packages('ggplot2')
# install.packages(c("Factoshiny","missMDA","FactoInvestigate"))
# install.packages('vcd')
# install.packages('ca')
# install.packages('table1')
# install.packages('pivottabler')
# install.packages('data.table')
# install.packages('vcd')

library(pollster)
library(dplyr)
library(knitr)
library('ggplot2')
library("FactoMineR")
library("factoextra")
library(ca)
library(dplyr)
library(grid)
library('vcd')

dados = prf_not_rain_data_correspondencia

dados <- subset(dados, select = -c(X))

dados <- lapply(dados, as.factor) %>% 
  data.frame


res_mca <- MCA(dados, graph = FALSE)

fviz_mca_var(res_mca, repel=TRUE, select.var = list(contrib = 20),
             shape.var = 2)

fviz_mca_var(res_mca, repel=TRUE, choice='mca.cor',
             shape.var = 2)

fviz_eig(res_mca, addlabels = TRUE)

fviz_mca_ind(res_mca, 
             label = "none", # hide individual labels
             habillage = c( 'condicao_metereologica'), # color by groups 
             addEllipses = TRUE,
             ggtheme = theme_minimal()) 
