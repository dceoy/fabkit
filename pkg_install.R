#!/usr/bin/env R
#
# pkg_install.R
#

# CRAN
pload <- function(p) {
  if (! p %in% installed.packages()[,1]) install.packages(p, dependencies = TRUE)
  require(p, character.only = TRUE)
}

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
          'MCMCpack',
          'RSQLite')
sapply(pkgs, pload)


# Stan
if (! 'rstan' %in% installed.packages()[,1]) {
  Sys.setenv(MAKEFLAGS = '-j4')
  source('http://mc-stan.org/rstan/install.R', echo = TRUE, max.deparse.length = 2000)
  install_rstan()
}
