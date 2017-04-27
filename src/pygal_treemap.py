# encoding=utf-8
import pandas as pd
import pygal
import sys
import os
import webbrowser

if len(sys.argv) > 1 and sys.argv[1] == "-test":
    df = pd.read_csv("~/Datasets/DRUG1N.csv")
    cat_field = "Drug"
    value_field = ""
    output_option = 'output_to_screen'
    output_path = '/Users/McCarroll/test/test.svg'
    output_width = 256
    output_height = 256
    viewer_command = ""
    title = "Test"
else:
    from pyspark.context import SparkContext
    from pyspark.sql.context import SQLContext
    import spss.pyspark.runtime
    ascontext = spss.pyspark.runtime.getContext()
    sc = ascontext.getSparkContext()
    sqlCtx = ascontext.getSparkSQLContext()
    df = ascontext.getSparkInputData().toPandas()
    cat_field = '%%category_field%%'
    value_field = '%%value_field%%'
    output_option = '%%output_option%%'
    output_path = '%%output_path%%'
    output_width = int('%%output_width%%')
    output_height = int('%%output_height%%')
    viewer_command = '%%viewer_command%%'
    title = '%%title%%'

if not value_field:
    value_field = '__value__'
    df[value_field] = 1

df = df[[cat_field,value_field]].groupby([cat_field], as_index=False).sum()


from pygal import Config

config = Config()
config.width = output_width
config.height = output_height
treemap = pygal.Treemap(config)
treemap.title = title

for i in df.index:
    cat = df.ix[i][cat_field]
    val = df.ix[i][value_field]
    treemap.add(cat, [val])

if output_option == 'output_to_file':
    if not output_path:
        raise Exception("No output path specified")
else:
    output_path = os.tempnam()+".svg"

treemap.render_to_file(output_path)

if output_option == 'output_to_screen':
    if viewer_command:
        os.system(viewer_command+" "+output_path)
    else:
        webbrowser.open("file://"+output_path)
    print("Output should now open in a browser window")
else:
    print("Output should be saved on the server to path: "+output_path)

