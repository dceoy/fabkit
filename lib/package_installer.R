#!/usr/bin/env Rscript

require_v <- function(pkgs) {
  return(sapply(as.vector(pkgs), require, character.only = TRUE))
}

cran_install <- function(pkgs, cran_repos = getOption('repos'), r_lib = .libPaths()[1]) {
  if(require('devtools')) {
    withr::with_libpaths(r_lib,
                         devtools::update_packages(pkgs = pkgs, repos = cran_repos, dependencies = TRUE))
  } else {
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      update.packages(instPkgs = pp, repos = cran_repos, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib)
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      install.packages(pkgs = pd, repos = cran_repos, lib = r_lib, dependencies = TRUE)
    }
  }
}

devt_install <- function(pkgs, host, cran_repos = getOption('repos'), r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('devtools')) {
    withr::with_libpaths(r_lib,
                         switch(host,
                                'cran' = devtools::install_cran(pkgs, repos = cran_repos, dependencies = TRUE),
                                'github' = devtools::install_github(pkgs),
                                'bitbucket' = devtools::install_bitbucket(pkgs)))
  }
}

drat_install <- function(pkgs, drat_repos, cran_repos = getOption('repos'), r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('drat')) {
    options(repos = cran_repos)
    drat:::addRepo(drat_repos)
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      update.packages(instPkgs = pp, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib)
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      install.packages(pkgs = pd, lib = r_lib, dependencies = TRUE)
    }
  }
}

bioc_install <- function(pkgs, r_lib = .libPaths()[1]) {
  if(! is.null(pkgs)) {
    options(BioC_mirror = 'https://bioconductor.org')
    if(! 'biocLite' %in% ls()) source('https://bioconductor.org/biocLite.R')
    biocLite(pkgs = pkgs, ask = FALSE, lib.loc = r_lib)
  }
}

install_by_list <- function(cfg, r_lib = .libPaths()[1]) {
  options(repos = cfg$repos$cran)
  lapply(union(util <- c('devtools', 'drat'), cfg$cran), function(p) try(cran_install(p)))
  devtools::has_devel()
  lapply(do.call(c, cfg$github), function(p) try(devt_install(p, host = 'github')))
  lapply(cfg$drat, function(p) try(drat_install(p, drat_repos = cfg$repos$drat)))
  lapply(cfg$bioconductor, function(p) try(bioc_install(p)))
  return(sapply(list(Utility = util,
                     CRAN = cfg$cran,
                     GitHub = names(cfg$github),
                     Drat = cfg$drat,
                     Bioconductor = cfg$bioc),
                require_v))
}

if(length(argv <- commandArgs(trailingOnly = TRUE)) > 0) {
  if(! require('yaml')) cran_install('yaml', cran_repos = 'https://cran.rstudio.com/')
  print(install_by_list(cfg = yaml::yaml.load_file(input = argv[1])))
}
