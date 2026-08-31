#!/usr/bin/env Rscript
# Deterministic structure audit for Hewitt et al. 2026 Code Ocean capsule.
# No model calls. Reads the public capsule's released RDS files and records the
# fields needed to reproduce open-model treatment-effect estimates.

args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 2) stop("usage: audit_capsule.R CAPSULE_DIR OUT_DIR")
root <- normalizePath(args[[1]])
out <- args[[2]]
dir.create(out, recursive=TRUE, showWarnings=FALSE)

data_dir <- file.path(root, "data")
llm_path <- file.path(data_dir, "llm_responses.RDS")
rct_path <- file.path(data_dir, "rct_responses.RDS")
if (!file.exists(llm_path)) stop(paste("missing", llm_path))
if (!file.exists(rct_path)) stop(paste("missing", rct_path))

llm <- readRDS(llm_path)
rct <- readRDS(rct_path)

sink(file.path(out, "structure.txt"))
cat("CAPSULE_DIR\n", root, "\n\n")
cat("llm_responses class:\n"); print(class(llm))
cat("llm_responses dim:\n"); print(dim(llm))
cat("llm_responses names:\n"); print(names(llm))
cat("llm_responses str(max.level=1):\n"); str(llm, max.level=1)
cat("\nfirst rows selected scalar columns:\n")
scalar_names <- names(llm)[vapply(llm, function(x) !is.list(x), logical(1))]
print(utils::head(llm[, scalar_names, drop=FALSE], 8))
cat("\nrct_responses class:\n"); print(class(rct))
cat("rct_responses dim:\n"); print(dim(rct))
cat("rct_responses names:\n"); print(names(rct))
cat("rct_responses str(max.level=2):\n"); str(rct, max.level=2)
sink()

# Model-level counts and coverage from released LLM responses.
model_col <- if ("model" %in% names(llm)) "model" else stop("model column missing")
models <- sort(unique(as.character(llm[[model_col]])))
model_counts <- data.frame(model=models, n_rows=as.integer(table(factor(llm[[model_col]], levels=models))))
if ("study" %in% names(llm)) {
  model_counts$n_studies <- vapply(models, function(m) length(unique(llm$study[llm$model==m])), integer(1))
}
if ("outcome.name" %in% names(llm)) {
  model_counts$n_outcomes <- vapply(models, function(m) length(unique(paste(llm$study[llm$model==m], llm$outcome.name[llm$model==m], sep="|||"))), integer(1))
}
if ("condition.name" %in% names(llm)) {
  model_counts$n_cells <- vapply(models, function(m) length(unique(paste(llm$study[llm$model==m], llm$condition.name[llm$model==m], sep="|||"))), integer(1))
}
write.csv(model_counts, file.path(out, "model_counts.csv"), row.names=FALSE)

# Write compact unique-value/count diagnostics for fields likely used in the
# released aggregation code. This prevents guessing at semantics from schema.
fields <- intersect(c("samples","expectation","weight","scale.min","scale.max","scale_min","scale_max"), names(llm))
sink(file.path(out, "aggregation_fields.txt"))
for (nm in fields) {
  cat("FIELD", nm, "\n")
  x <- llm[[nm]]
  cat("class:", paste(class(x), collapse=","), "\n")
  if (is.numeric(x)) {
    print(summary(x))
  } else {
    print(utils::head(sort(table(as.character(x)), decreasing=TRUE), 30))
  }
  cat("\n")
}
sink()

# Export a tiny, deterministic sample for understanding one complete study cell.
if (all(c("study","condition.name","outcome.name") %in% names(llm))) {
  keys <- unique(data.frame(study=as.character(llm$study), condition=as.character(llm$condition.name), outcome=as.character(llm$outcome.name), stringsAsFactors=FALSE))
  keys$key <- paste(keys$study, keys$condition, keys$outcome, sep="|||")
  keys <- keys[order(keys$key),]
  k <- keys[1,]
  idx <- llm$study==k$study & llm$condition.name==k$condition & llm$outcome.name==k$outcome
  small <- llm[idx, scalar_names, drop=FALSE]
  if (nrow(small)>100) small <- small[1:100,]
  write.csv(small, file.path(out,"first_cell_sample.csv"), row.names=FALSE)
}

# Preserve released licenses if present.
for (nm in c("LICENSE", "LICENSE.txt")) {
  p <- file.path(data_dir,nm); if (file.exists(p)) file.copy(p, file.path(out,paste0("data_",nm)), overwrite=TRUE)
  p2 <- file.path(root,"code",nm); if (file.exists(p2)) file.copy(p2, file.path(out,paste0("code_",nm)), overwrite=TRUE)
}

cat("audit complete\n")
