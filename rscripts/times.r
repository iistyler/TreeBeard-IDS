#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("Usage: Rscript times.r [time data file]")
} else if (length(args) >= 1) {
	fname = args[1]
}

data <- read.csv(fname, header=TRUE, dec=".")
attach(data)
mtime = mean(Time)

jpeg("time-boxplot.jpg")
boxplot(Time ~ Layer, data=data, main="Cumulative Time per Layer", 
		xlab="Layers Used to Classify Connection", ylab="Time (Seconds)")

abline(h=mtime, col="red", lty=2)

legend( x = 0.5, y = max(Time), c("Mean Classification Time"), col="red", pch=22, lty=2)

