因为 vcf 文件的统计涉及到较多的代码和命令，特在此说明。
### 只做基础统计(会输出简短vcf文件和基因型文件)
```
python vcf_stat.py -f test.vcf -p false
```
stat.txt 文件内容
```
The number of samples: 10
The number of SNP: 173719
Heterozygosity rate per sample:
    QF190327001: 15.38%
    QF190322003: 37.35%
    QF190322007: 34.73%
    QF190322009: 53.54%
    QF190322008: 49.82%
    QF190322010: 47.76%
    QF190322002: 50.08%
    QF190322006: 11.09%
    QF190322004: 36.60%
    QF190402001: 50.72%
The number of variation type:
    C --> G: 5400
    G --> C: 5478
    A --> C: 8364
    T --> G: 8674
    C --> A: 10125
    G --> T: 10547
    A --> T: 13106
    T --> A: 13247
    T --> C: 22254
    A --> G: 22491
    C --> T: 26945
    G --> A: 27088
```
### 做基础统计的同时，做变异类型条形图和热图
```
python vcf_stat.py -f test.vcf
```
![](https://i.loli.net/2021/01/21/hEBSzkOqmTUAJQ7.jpg)

### 做基础统计的同时，做区间单倍型图
```
python vcf_stat.py -f test.vcf -p false --start 1 --end 1000
python vcf_stat.py -f test.vcf -p false --start 1 --end 1000 --sample_name order.txt # 指定单倍型图的样本顺序
# order.txt 文件每行按需求顺序填写一个样本
```
![](https://i.loli.net/2021/01/21/1QGAFJickO7zHxV.jpg)
