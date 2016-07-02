#!/usr/bin/env Rscript

require_v <- function(pkgs) {
  return(sapply(as.vector(pkgs), require, character.only = TRUE))
}

load_cran <- function(pkgs, cran_repos, r_lib = .libPaths()[1]) {
  if(! is.null(pkgs)) {
    options(repos = cran_repos)
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      if(require('devtools')) {
        try(withr::with_libpaths(r_lib, update_packages(pp, dependencies = TRUE)))
      } else {
        try(update.packages(instPkgs = pp, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib))
      }
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      try(install.packages(pkgs = pd, lib = r_lib, dependencies = TRUE))
    }
    return(require_v(pkgs))
  }
}

load_dev <- function(pkgs, host = 'github', r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('devtools')) {
    try(withr::with_libpaths(r_lib,
                             switch(host,
                                    'github' = install_github(do.call(c, pkgs)),
                                    'bitbucket' = install_bitbucket(do.call(c, pkgs)))))
    return(require_v(names(pkgs)))
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

update_env <- function(cfg, r_lib = .libPaths()[1]) {
  Sys.setenv(MAKEFLAGS = paste0('-j', parallel::detectCores()))
  load_cran(union(util <- c('yaml', 'devtools', 'drat'), cfg$cran), cran_repos = cfg$repos$cran)
  load_dev(cfg$github, host = 'github')
  load_drat(cfg$drat, drat_repos = cfg$repos$drat, cran_repos = cfg$repos$cran)
  load_bioc(cfg$bioconductor)
  return(sapply(list(Utility = util,
                     CRAN = cfg$cran,
                     GitHub = names(cfg$github),
                     Drat = cfg$drat,
                     Bioconductor = cfg$bioc),
                require_v))
}

if(length(argv <- commandArgs(trailingOnly = TRUE)) > 0) {
  load_cran('yaml', cran_repos = 'https://cran.rstudio.com/')
  print(update_env(cfg = yaml.load_file(input = argv[1])))
}
