#!/usr/bin/env Rscript


# CRAN
options(repos = "http://cran.rstudio.com/")
update.packages(checkBuilt = TRUE, ask = FALSE)

pkgs <- c('dplyr',
          'tidyr',
          'data.table',
          'devtools',
          'yaml',
          'snow',
          'foreach',
          'doSNOW',
          'ggplot2',
          'ggmcmc',
          'glmmML',
          'MCMCpack',
          'abc',
          'phangorn',
          'rstan',
          'RSQLite')
sapply(pkgs,
       function(p) {
         if (! p %in% installed.packages()[,1]) install.packages(p, dependencies = TRUE)
         require(p, character.only = TRUE)
       })
