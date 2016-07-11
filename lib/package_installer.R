#!/usr/bin/env Rscript

cran_install <- function(pkgs = NULL, repos = getOption('repos'), r_lib = .libPaths()[1]) {
  if(require('devtools')) {
    try(withr::with_libpaths(r_lib,
                             devtools::update_packages(pkgs = pkgs, repos = repos, dependencies = TRUE)))
  } else {
    if(length(pp <- intersect(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      try(update.packages(instPkgs = pp, repos = repos, checkBuilt = TRUE, ask = FALSE, lib.loc = r_lib))
    }
    if(length(pd <- setdiff(pkgs, installed.packages(lib.loc = r_lib)[, 1])) > 0) {
      try(install.packages(pkgs = pd, repos = repos, lib = r_lib, dependencies = TRUE))
    }
  }
}

devtools_install <- function(pkgs, host = 'github', repos = getOption('repos'), r_lib = .libPaths()[1]) {
  if(! is.null(pkgs) && require('devtools')) {
    try(withr::with_libpaths(r_lib,
                             switch(host,
                                    'cran' = devtools::install_cran(pkgs, repos = repos, dependencies = TRUE),
                                    'github' = devtools::install_github(pkgs),
                                    'bitbucket' = devtools::install_bitbucket(pkgs))))
  }
}

bioc_install <- function(pkgs, mirror = 'https://bioconductor.org', r_lib = .libPaths()[1]) {
  if(! is.null(pkgs)) {
    options(BioC_mirror = mirror)
    if(! 'biocLite' %in% ls()) source(paste0(mirror, '/biocLite.R'))
    try(biocLite(pkgs = pkgs, ask = FALSE, lib.loc = r_lib))
  }
}

test_load <- function(pkgs) {
  v_status <- suppressMessages(sapply(as.vector(pkgs), require, character.only = TRUE))
  if(require('devtools')) {
    message()
    print(devtools::session_info())
  }
  message('\nLoading test -------------------------------------------------------------------')
  if(length(v_succeeded <- names(v_status)[v_status]) > 0) {
    message(' Succeeded:')
    message(paste0(paste0('  ', v_succeeded), collapse = '\n'))
  }
  if(length(v_failed <- names(v_status)[! v_status]) > 0) {
    message(' Failed:')
    message(paste0(paste0('  ', v_failed), collapse = '\n'))
  }
  message()
}

install_by_list <- function(cfg, r_lib = .libPaths()[1]) {
  options(repos = c(CRAN = cfg$repos$cran))
  cran_install(util <- c('devtools', 'drat'))
  sapply(util, require, character.only = TRUE)
  drat:::addRepo(account = cfg$repos$drat)
  lapply(c(cfg$cran, cfg$drat), cran_install)
  lapply(do.call(c, cfg$github), devtools_install)
  lapply(cfg$bioconductor, bioc_install)
  test_load(c(cfg$cran, names(cfg$github), cfg$drat, cfg$bioconductor))
}

if(length(argv <- commandArgs(trailingOnly = TRUE)) > 0) {
  if(! require('yaml')) cran_install('yaml', repos = 'https://cran.rstudio.com/')
  install_by_list(cfg = yaml::yaml.load_file(input = argv[1]))
}
