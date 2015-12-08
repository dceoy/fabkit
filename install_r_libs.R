#!/usr/bin/env Rscript

options(repos = 'http://cran.rstudio.com/', BioC_mirror = 'https://bioconductor.org')
r_lib <- .libPaths()[1]
installed_pkgs <- installed.packages(lib.loc = r_lib)[, 1]
source('https://bioconductor.org/biocLite.R')

require_v <- function(pkgs) {
  return(sapply(as.vector(pkgs),
                function(pkg) return(require(pkg, character.only = TRUE))))
}

load_cran <- function(pkgs) {
  if(length(pp <- intersect(pkgs, installed_pkgs)) != 0) {
    if(require_v('devtools')) {
      with_libpaths(r_lib, update_packages(pp, dependencies = TRUE))
    } else {
      update.packages(instPkgs = pp, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib)
    }
  }
  if(length(pd <- setdiff(pkgs, installed_pkgs)) != 0) {
    install.packages(pkgs = pd, lib = r_lib, dependencies = TRUE)
  }
  return(require_v(pkgs))
}

load_dev <- function(pkgs, host = 'github') {
  if(require_v('devtools')) {
    with_libpaths(r_lib,
                  switch(host,
                         'github' = install_github(names(pkgs)),
                         'bitbucket' = install_bitbucket(names(pkgs))))
  }
  return(require_v(pkgs))
}

load_bioc <- function(pkgs) {
  try(biocLite(pkgs = pkgs, ask = FALSE, lib.loc = r_lib))
  return(require_v(pkgs))
}

if(length(installed_pkgs) == 0) {
  load_cran('devtools')
} else {
  load_cran(union('devtools', installed_pkgs))
  try(biocLite('BiocUpgrade', ask = FALSE, lib.loc = r_lib))
}

ls_pkgs <- list(cran = c('dplyr',
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
                         'broom',
                         'caret',
                         'leaflet',
                         'plyr',
                         'shiny',
                         'rvest',
                         'rbenchmark',
                         'rmarkdown'),
                github = c('klutometis/roxygen' = 'roxygen2',
                           'rstudio/httpuv' = 'httpuv'),
                bioc = c('BiocInstaller',
                         'PhViD',
                         'Biobase',
                         'GEOquery'))

print(list(CRAN = c(require_v('devtools'),
                    load_cran(ls_pkgs$cran)),
           GitHub = load_dev(ls_pkgs$github),
           Bioconductor = load_bioc(ls_pkgs$bioc)))
