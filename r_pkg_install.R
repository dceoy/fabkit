#!/usr/bin/env Rscript


# CRAN
options(repos = 'http://cran.rstudio.com/')
update.packages(checkBuilt = TRUE, ask = FALSE)

pkg_load <- function(p) {
  if (! p %in% installed.packages()[, 1]) install.packages(p, dependencies = TRUE)
  require(p, character.only = TRUE)
}

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
          'gridExtra',
          'glmmML',
          'MCMCpack',
          'coin',
          'abc',
          'phangorn',
          'rstan',
          'RSQLite')

print(sapply(pkgs, pkg_load))
