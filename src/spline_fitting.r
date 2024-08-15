library(GenWin)
library(here)
chr1 <- read.csv("../data/ACC001_vs_ACC041/chr/fst/ACC001_vs_ACC041_chr1_fst-fst-1_bp_windows.csv")
chr2 <- read.csv("../data/ACC001_vs_ACC041/chr/fst/ACC001_vs_ACC041_chr2_fst-fst-1_bp_windows.csv")
# data <- chr1[0:8000,]
data <- chr2
pdf(file=here("spline.pdf"))
print(nrow(data))

str(data)
result <- splineAnalyze(
    Y=data$ACC001_vs_ACC041,
    map=data$pos_ini,
    smoothness=10,
    plotRaw=TRUE,
    plotWindows=TRUE,
    method=4
)

write.table(result$breaks, file = "spline_breaks", row.names = FALSE, col.names = FALSE, quote = FALSE)
write.csv(result$windowData, file = "spline_fst.csv", row.names = FALSE)
