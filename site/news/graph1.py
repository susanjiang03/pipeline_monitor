
#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N=6

df=pd.DataFrame({'business':[5, 25, 18, 30, 10,16],
                'technology':[10, 14, 19, 30,9,24],
                 'politics':[7, 22, 12, 20,36,13],
                'sports':[18, 25, 30, 6,20,17],
                'environment':[30, 22, 14, 19,28,10],
                'health':[15, 22, 14, 19,28,10]},
columns=['business','technology','politics','sports','environment','health'])

df.plot(kind='bar',stacked=True,width=0.35,color=['#0000FF','#0080FF','#81BEF7',
 
                                                  '#00FFBF','#40FF00','#F4FA58'])




plt.ylabel('Number of rss feed',fontsize=15)
plt.title('Compare number of RSS Feed of different newspapers',fontsize=30,fontweight='bold')
ax=plt.subplot()
ax.set_xticklabels(('New York Times', 'Los Angeles Time', 'The Washington Post', 'Chicago Tribute', 'The Boston Globe','Philadephia Inquirer'),rotation=30,fontsize=20,fontweight='bold')
plt.legend()
plt.show()