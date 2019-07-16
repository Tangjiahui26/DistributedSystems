plot
================
Jiahui Tang
2019-06-02

Get the data
------------

``` r
data <- read.xls("/Users/tangjiahui/Desktop/result.xlsx",sheet=1,na.strings=c("NA","#DIV/0!"))
print(data)
```

    ##       Node Percent      Results
    ## 1  “3 VMs”    0.02 0.0006250000
    ## 2  “3 VMs”    0.02 0.0005847953
    ## 3  “3 VMs”    0.02 0.0005882353
    ## 4  “3 VMs”    0.02 0.0005750431
    ## 5  “3 VMs”    0.02 0.0005555556
    ## 6  “3 VMs”    0.10 0.0016051364
    ## 7  “3 VMs”    0.10 0.0014716703
    ## 8  “3 VMs”    0.10 0.0018518519
    ## 9  “3 VMs”    0.10 0.0013888889
    ## 10 “3 VMs”    0.10 0.0016207455
    ## 11 “3 VMs”    0.30 0.0387096774
    ## 12 “3 VMs”    0.30 0.0383333333
    ## 13 “3 VMs”    0.30 0.0369230769
    ## 14 “3 VMs”    0.30 0.0371428571
    ## 15 “3 VMs”    0.30 0.0375586854
    ## 16 “4 VMs”    0.02 0.0004347826
    ## 17 “4 VMs”    0.02 0.0004166667
    ## 18 “4 VMs”    0.02 0.0004545455
    ## 19 “4 VMs”    0.02 0.0004000000
    ## 20 “4 VMs”    0.02 0.0004291845
    ## 21 “4 VMs”    0.10 0.0019762846
    ## 22 “4 VMs”    0.10 0.0020408163
    ## 23 “4 VMs”    0.10 0.0018348624
    ## 24 “4 VMs”    0.10 0.0020833333
    ## 25 “4 VMs”    0.10 0.0021052632
    ## 26 “4 VMs”    0.30 0.0417827298
    ## 27 “4 VMs”    0.30 0.0384615385
    ## 28 “4 VMs”    0.30 0.0406250000
    ## 29 “4 VMs”    0.30 0.0428571429
    ## 30 “4 VMs”    0.30 0.0436046512

``` r
data_cal <- summarySE(data, measurevar="Results", groupvars=c("Node", "Percent"))
print(data_cal)
```

    ##      Node Percent N      Results           sd           se           ci
    ## 1 “3 VMs”    0.02 5 0.0005857259 2.536725e-05 1.134458e-05 3.149760e-05
    ## 2 “3 VMs”    0.10 5 0.0015876586 1.761824e-04 7.879117e-05 2.187594e-04
    ## 3 “3 VMs”    0.30 5 0.0377335261 7.663105e-04 3.427045e-04 9.515001e-04
    ## 4 “4 VMs”    0.02 5 0.0004270359 2.037072e-05 9.110062e-06 2.529359e-05
    ## 5 “4 VMs”    0.10 5 0.0020081120 1.086216e-04 4.857704e-05 1.348715e-04
    ## 6 “4 VMs”    0.30 5 0.0414662125 2.021354e-03 9.039772e-04 2.509843e-03

Plot the data using ggplot
--------------------------

``` r
pd <- position_dodge(0.001)
plot1 <- ggplot(data_cal, aes(x=Percent, y=Results, colour=Node)) + 
    geom_errorbar(aes(ymin=Results-sd, ymax=Results+sd), width=.1, position=pd) +
    geom_line(position=pd) +
    geom_point(position=pd) +
    xlab("Message Loss Rate") +
    ylab("False Positive Rate") +
    theme_bw() +
    ggtitle("Average FP rate \nwith Standard Deviation") +
    theme(legend.position = c(0.8, 0.3))
```

``` r
plot2<- ggplot(data_cal, aes(x=Percent, y=Results, colour=Node)) + 
    geom_errorbar(aes(ymin=Results-ci, ymax=Results+ci), width=.1, position=pd) +
    geom_line(position=pd) +
    geom_point(position=pd) +
    xlab("Message Loss Rate") +
    ylab("False Positive Rate") +
    theme_bw() +
    ggtitle("Average FP rate \nwith 95% Confidence Interval") +
    theme(legend.position = c(0.8, 0.3))
plot_grid(plot1, plot2, labels = "AUTO")
```

    ## Warning: position_dodge requires non-overlapping x intervals

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning: position_dodge requires non-overlapping x intervals

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201c

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): font
    ## metrics unknown for Unicode character U+201d

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_stringMetric, as.graphicsAnnot(x$label)): conversion
    ## failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“3 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9c>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <e2>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <80>

    ## Warning in grid.Call(C_textBounds, as.graphicsAnnot(x$label), x$x, x$y, :
    ## conversion failure on '“4 VMs”' in 'mbcsToSbcs': dot substituted for <9d>

![](plot_files/figure-markdown_github-ascii_identifiers/options(warn=-1)-1.png)
