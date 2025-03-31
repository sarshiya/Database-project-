#install.packages("DESeq2")
library(DESeq2)
library(tibble)
library(dplyr)
library(readxl)
#install.packages('pheatmap')
library(pheatmap)


setwd('/projectnb/rd-spat/HOME/abhyuday/new_folder')


#' Load a tsv located at specific location `filename` into a tibble
#'
#'
#' @param filename (str): the path to a specific file (ie 'file/path/to/file.tsv')
#'
#' @return tibble: a (g x 1+m) tibble with a 'gene' column followed by
#' sample names as column names.
#'
#' @note Column 'gene' should be first and the only column to contain strings.
#' Data in sample_name columns CANNOT be strings
#'
#' @example `verse_counts <- read_data('verse_counts.tsv')`

read_data <- function(filename){
  a= read_csv(filename)
  a
  
}

counts=read_data('placenta_opioid_counts.csv')
meta=read_excel('placenta_opioid_meta.xlsx')
head(counts)
head(meta)

#' Filter out genes with zero variance
#'
#'
#' @param verse_counts tibble: a (g x 1+m) tibble with a 'gene' column followed
#' by m raw counts columns with sample names as column names.
#'
#' @return tibble: a (n x 1+m) tibble with a 'gene' column followed by m columns
#' of raw counts with genes that have zero variance across samples removed
#'
#' @note (g >= n)
#'
#' @example `filtered_counts <- filter_zero_var_genes(verse_counts)`

filter_zero_var_genes <- function(verse_counts) {
  verse_counts %>%
    filter(!apply(select(., -Genes), 1, var) == 0)
}

# Create a heatmap---pheatmap(counts_filterd, cluster_rows = TRUE, cluster_cols = TRUE)

counts_filterd=filter_zero_var_genes(counts)
colnames(counts_filterd)

head(meta)



#' Calculate total read counts for each sample in a count data.
#'
#'
#' @param count_data tibble: a (n x 1+m) tibble with a 'gene' column followed
#' by m raw counts columns of read counts
#'
#' @return tibble or named vector of read totals from each sample. Vectors must
#' be length `_S_ `, a tibble can be `(1 x _S_)` with sample names as columns
#' names OR `(_S_ x 2)` with columns ("sample", "value")
#'
#' @examples `get_library_size(count_data)`

get_library_size <- function(count_data) {
  new=count_data[,-1]
  p=colnames(new)
  q=colSums(new)
  a=tibble(Sample_name=p,library_size=q)
  a
  
}

lib_size_counts=get_library_size(counts_filterd)



# Convert count data to a matrix
counts_filterd= counts_filterd %>% column_to_rownames(var='Genes')
count_matrix <- as.matrix(counts_filterd)

# Convert specific variables to factors in the metadata
meta$OPIOIDCONTROL <- factor(meta$OPIOIDCONTROL)
meta$RACE <- factor(meta$RACE)
meta$OPIOIDTYPE <- factor(meta$OPIOIDTYPE)
meta$SEX <- factor(meta$SEX)
meta$ETHNICITY = factor(meta$ETHNICITY)


# Create DESeqDataSet object
dds <- DESeqDataSetFromMatrix(countData = round(count_matrix),
                              colData = meta,
                              design = ~ OPIOIDCONTROL + RACE +SEX + ETHNICITY )


# Estimate size factors
dds <- estimateSizeFactors(dds)

# Perform DESeq2 analysis
#dds <- DESeq(dds)

dds <- DESeq(dds, betaPrior = TRUE)

# Get differential expression results
res <- results(dds)

# Summary of differential expression results
summary(res)
head(res)

# Volcano plot
plotMA(res)

# MA plot
plotMA(res, alpha = 0.05)

res_2 <- res[!is.na(res$log2FoldChange), ]
# Create a heatmap
pheatmap(counts_filterd, cluster_rows = TRUE, cluster_cols = TRUE)




