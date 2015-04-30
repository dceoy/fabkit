#!/usr/bin/env R
#
# pkg_install.R
#

pload <- function(p) {
  if (! p %in% installed.packages()[,1]) install.packages(p, dependencies = TRUE)
  require(p, character.only = TRUE)
}

r <- getOption('repos')
r['CRAN'] <- 'http://cran.us.r-project.org'
options(repos = r)

ps <- c('RSQLite',
        'dplyr',
        'tidyr',
        'data.table',
        'yaml',
        'snow',
        'parallel',
        'foreach',
        'doSNOW',
        'ggplot2',
        'ggmcmc',
        'MCMCpack')
sapply(ps, pload)

if (! 'rstan' %in% installed.packages()[,1]) {
  Sys.setenv(MAKEFLAGS = '-j4')
  source('http://mc-stan.org/rstan/install.R', echo = TRUE, max.deparse.length = 2000)
  install_rstan()
}
require('rstan')
