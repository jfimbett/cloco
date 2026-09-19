# Path helpers backed by data/registry.json. From any script:
#   source("code/utils/data_paths.R")
#   df <- arrow::read_parquet(data_path("crsp_msf_2000_2023"))
#   arrow::write_parquet(df, out_path("panel_clean", stage = "processed", depends_on = "crsp_msf_2000_2023"))
# Never write literal Dropbox / home-directory paths in analysis code.

.cloco_root <- function() {
  d <- getwd()
  for (i in 1:6) {
    if (file.exists(file.path(d, "data", "registry.json"))) return(d)
    d <- dirname(d)
  }
  stop("data/registry.json not found above the working directory")
}

.cloco_env <- function() {
  root <- .cloco_root()
  env <- list(PROJECT_ROOT = root)
  f <- file.path(root, ".env")
  if (file.exists(f)) {
    for (ln in readLines(f, warn = FALSE)) {
      ln <- trimws(ln)
      if (ln == "" || startsWith(ln, "#") || !grepl("=", ln)) next
      kv <- strsplit(ln, "=", fixed = TRUE)[[1]]
      val <- trimws(paste(kv[-1], collapse = "="))
      if (val != "") env[[trimws(kv[1])]] <- path.expand(gsub("^['\"]|['\"]$", "", val))
    }
  }
  for (v in c("DROPBOX_ROOT", "DATA_ROOT")) {
    sysv <- Sys.getenv(v, unset = "")
    if (sysv != "") env[[v]] <- path.expand(sysv)
  }
  if (is.null(env$DROPBOX_ROOT)) {
    for (g in c("~/Dropbox", "~/Library/CloudStorage/Dropbox")) if (dir.exists(path.expand(g))) { env$DROPBOX_ROOT <- path.expand(g); break }
  }
  env
}

.cloco_resolve <- function(template) {
  env <- .cloco_env()
  vars <- regmatches(template, gregexpr("\\$\\{[A-Z0-9_]+\\}", template))[[1]]
  for (v in unique(vars)) {
    key <- gsub("[${}]", "", v)
    if (is.null(env[[key]])) stop(sprintf("%s not set in .env (see .env.example)", v))
    template <- gsub(v, env[[key]], template, fixed = TRUE)
  }
  if (!grepl("^(/|[A-Za-z]:)", template)) template <- file.path(env$PROJECT_ROOT, template)
  normalizePath(template, mustWork = FALSE)
}

data_path <- function(name, must_exist = TRUE) {
  if (requireNamespace("jsonlite", quietly = TRUE)) {
    reg <- jsonlite::fromJSON(file.path(.cloco_root(), "data", "registry.json"), simplifyVector = FALSE)
    if (is.null(reg$datasets[[name]])) stop(sprintf("'%s' is not in data/registry.json — register it with /data-registry add", name))
    p <- .cloco_resolve(reg$datasets[[name]]$path)
  } else {  # no jsonlite: ask the registry CLI to resolve the path
    p <- suppressWarnings(system2("python3", shQuote(c(file.path(.cloco_root(), ".claude/scripts/data_registry.py"), "where", name)), stdout = TRUE, stderr = FALSE))
    if (length(p) == 0 || !nzchar(p[1])) stop(sprintf("'%s' is not in data/registry.json (or a ${ROOT} is unset in .env)", name))
    p <- p[1]
  }
  if (must_exist && !file.exists(p)) stop(sprintf("%s is registered at %s but the file is not on this machine", name, p))
  p
}

out_path <- function(name, stage = "processed", fmt = "parquet", root = "${PROJECT_ROOT}",
                     depends_on = NULL, source = NULL, register = TRUE) {
  template <- if (root == "${PROJECT_ROOT}") sprintf("%s/data/%s/%s.%s", root, stage, name, fmt) else sprintf("%s/%s.%s", root, name, fmt)
  p <- .cloco_resolve(template)
  dir.create(dirname(p), recursive = TRUE, showWarnings = FALSE)
  if (register) {
    script <- tryCatch(basename(sys.frame(1)$ofile), error = function(e) "R session")
    args <- c(file.path(.cloco_root(), ".claude/scripts/data_registry.py"), "add", name, "--path", template,
              "--stage", stage, "--source", if (is.null(source)) paste("produced by", script) else source,
              "--format", fmt, "--force")
    if (!is.null(depends_on)) args <- c(args, "--depends", depends_on)
    system2("python3", shQuote(args), stdout = FALSE, stderr = FALSE)
  }
  p
}
