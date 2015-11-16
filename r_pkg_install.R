#!/usr/bin/env Rscript

# cran
options(repos = 'http://cran.rstudio.com/')
if(length(list.files(.libPaths()[1])) != 0) update.packages(checkBuilt = TRUE, ask = FALSE)

# devtools
if(! 'devtools' %in% installed.packages()[, 1]) install.packages('devtools', dep = TRUE)

# bioconductor
source('http://bioconductor.org/biocLite.R')
biocLite()

# packages
df_pkg <- rbind(data.frame(name = c('dplyr',
                                    'tidyr',
                                    'data.table',
                                    'yaml',
                                    'snow',
                                    'foreach',
                                    'doSNOW',
                                    'ggplot2',
                                    'ggmcmc',
                                    'ggdendro',
                                    'gridExtra',
                                    'glmmML',
                                    'MCMCpack',
                                    'rstan',
                                    'coin',
                                    'ranger',
                                    'abc',
                                    'phangorn',
                                    'amap',
                                    'GMD',
                                    'RSQLite',
                                    'plyr',
                                    'shiny',
                                    'rvest',
                                    'rbenchmark',
                                    'rmarkdown'),
                           repos = 'cran'),
                data.frame(name = c('klutometis/roxygen'),
                           repos = 'github'),
                data.frame(name = c('PhViD',
                                    'Biobase',
                                    'GEOquery'),
                           repos = 'bioc'))

# install
apply(df_pkg,
      1,
      function(pkg) {
        if(! pkg['name'] %in% installed.packages()[, 1]) {
          switch(pkg['repos'],
                 'cran' = install.packages(pkg['name'], dep = TRUE),
                 'github' = devtools::install_github(pkg['name']),
                 'bioc' = biocLite(pkg['name']))
        }
      })

# load
print(sapply(as.vector(df_pkg$name),
             function(pkg) require(pkg, character.only = TRUE)))
