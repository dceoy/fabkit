#!/usr/bin/env Rscript

require_v <- function(pkgs) {
  return(sapply(as.vector(pkgs), require, character.only = TRUE))
}

load_cran <- function(pkgs, cran_repos, r_lib = .libPaths()[1]) {
  if(! is.null(pkgs)) {
    options(repos = cran_repos)
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      if(require('devtools')) {
        with_libpaths(r_lib, update_packages(pp, dependencies = TRUE))
      } else {
        update.packages(instPkgs = pp, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib)
      }
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      install.packages(pkgs = pd, lib = r_lib, dependencies = TRUE)
    }
    return(require_v(pkgs))
  }
}

load_dev <- function(pkgs, host = 'GitHub', r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('devtools')) {
    try(with_libpaths(r_lib,
                      switch(host,
                             'GitHub' = install_github(names(pkgs)),
                             'Bitbucket' = install_bitbucket(names(pkgs)))))
    return(require_v(pkgs))
  }
}

load_drat <- function(pkgs, drat_repos, cran_repos, r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('drat')) {
    options(repos = cran_repos)
    drat:::addRepo(drat_repos)
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      try(update.packages(instPkgs = pp, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib))
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      try(install.packages(pkgs = pd, lib = r_lib, dependencies = TRUE))
    }
    return(require_v(pkgs))
  }
}

load_bioc <- function(pkgs, r_lib = .libPaths()[1]) {
  if(! is.null(pkgs)) {
    options(BioC_mirror = 'https://bioconductor.org')
    source('https://bioconductor.org/biocLite.R')
    try(biocLite(pkgs = pkgs, ask = FALSE, lib.loc = r_lib))
    return(require_v(pkgs))
  }
}

update_env <- function(pkgs, repos, r_lib = .libPaths()[1]) {
  load_cran(union(util <- c('devtools', 'drat'), pkgs$CRAN), cran_repos = repos$CRAN)
  load_dev(pkgs$GitHub, host = 'GitHub')
  load_dev(pkgs$Bitbucket, host = 'Bitbucket')
  load_drat(pkgs$Drat, drat_repos = repos$Drat, cran_repos = repos$CRAN)
  load_bioc(pkgs$Bioconductor)
  return(print(sapply(c(list(Utility = util), pkgs), require_v)))
}

Sys.setenv(MAKEFLAGS = paste0('-j', parallel::detectCores()))
update_env(pkgs = list(CRAN = c('dplyr',
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
                                'glmnet',
                                'glmmML',
                                'MCMCpack',
                                'rstan',
                                'loo',
                                'coin',
                                'ranger',
                                'abc',
                                'phangorn',
                                'amap',
                                'GMD',
                                'RSQLite',
                                'h2o',
                                'tm',
                                'broom',
                                'caret',
                                'leaflet',
                                'plyr',
                                'shiny',
                                'rvest',
                                'rbenchmark',
                                'rmarkdown'),
                       GitHub = c('wesm/feather/R' = 'feather',
                                  'klutometis/roxygen' = 'roxygen2',
                                  'rstudio/httpuv' = 'httpuv'),
                       Drat = c('mxnet',
                                'xgboost'),
                       Bioconductor = c('BiocInstaller',
                                        'Biostrings',
                                        'PhViD',
                                        'Biobase',
                                        'GEOquery')),
           repos = list(CRAN = c('https://cran.rstudio.com/'),
                        Drat = c('dmlc')))
