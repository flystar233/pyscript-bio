import pandas as pd
df1 = pd.read_excel('/ldfssz1/MS_OP/USER/xutengfei1/spider_rna/SpiderA-VS-SpiderB.DEGseq_Method.GeneDiffExpFilter.xls')
df2 = pd.read_excel('/ldfssz1/MS_OP/USER/xutengfei1/spider_rna/annotation.xls')
outfile = pd.merge(df1, df2, how='left', left_on='GeneID',right_on='Unigene')
outfile.to_excel('outfile.xls', index=False)  
