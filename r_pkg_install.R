#!/usr/bin/env Rscript

# cran
options(repos = 'http://cran.rstudio.com/')
if(length(list.files(.libPaths()[1])) != 0) update.packages(checkBuilt = TRUE, ask = FALSE)
load_cr <- function(pkgs) {
  sapply(as.vector(pkgs),
         function(pkg) {
           if(! pkg %in% installed.packages()[, 1]) install.packages(pkg, dep = TRUE)
           require(pkg, character.only = TRUE)
         })
}

# devtools
load_cr('devtools')
load_gh <- function(pkgs) {
  devtools::install_github(pkgs)
  sapply(as.vector(names(pkgs)),
         function(pkg) {
           require(pkg, character.only = TRUE)
         })
}

# bioconductor
source('http://bioconductor.org/biocLite.R')
biocLite()
load_bc <- function(pkgs) {
  sapply(as.vector(pkgs),
         function(pkg) {
           if(! pkg %in% installed.packages()[, 1]) biocLite(pkg)
           require(pkg, character.only = TRUE)
         })
}

# install
pkgs <- list(cr = c('dplyr',
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
                    'h2o',
                    'plyr',
                    'shiny',
                    'rvest',
                    'rbenchmark',
                    'rmarkdown'),
             gh = c('roxygen2' = 'klutometis/roxygen',
                    'httpuv' = 'rstudio/httpuv'),
             bc = c('PhViD',
                    'Biobase',
                    'GEOquery'))
print(list(cran = load_cr(pkgs$cr),
           github = load_gh(pkgs$gh),
           bioconductor = load_bc(pkgs$bc)))
