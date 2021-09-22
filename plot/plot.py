import glob
import os
import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.rcParams.update({'figure.autolayout': True})
plt.rc('axes', axisbelow=True)

path = '~/bench_scripts/'

def plot(df, object_type, colors):
   df = df.groupby(['turbo', 'objects_no'])
   df = df['duration'].aggregate(np.mean).unstack()
   fig = plt.figure(figsize=(6, 4))
   ax = fig.add_subplot(1, 1, 1)
   
   g = df.T.plot.barh(ax=ax, capsize=4, rot=0, color=colors, edgecolor='black', linewidth=0.15)
   g.invert_yaxis()
   plt.ylabel(f'# of {object_type}s')
   plt.xlabel('Average Time (s)')
   from matplotlib.ticker import ScalarFormatter,AutoMinorLocator
   ax.xaxis.set_major_formatter(ScalarFormatter())
   ax.xaxis.major.formatter._useMathText = True
   ax.xaxis.set_minor_locator(  AutoMinorLocator(2))
   box = ax.get_position()
   ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
   ax.set_xlim(0, 800)

   # annotate
   for p in ax.patches:
      x = p.get_x() + p.get_width() + 0.02 + 0.7
      y = p.get_y() + p.get_height()/2 + 0.04
      ax.annotate(round(p.get_width(), 2), (x, y), fontsize=6, weight='bold', color=p.get_facecolor())

   # pad the spacing between the number and the edge of the figure
   axes = plt.gca()
   axes.xaxis.grid()   

   ax.set_title("Red Hat OpenShift Collection Benchmark", fontsize=10, color='grey')
   plt.legend(loc="best", fancybox=True,  ncol=2, frameon=True, title="Turbo mode")
   plt.savefig(f"{path}/{object_type}.png", dpi=600)


def filter_data(df, ns_count):
   return df[np.isin(df, [f'Create {ns_count} Namespace(s)', f'Create {ns_count} ConfigMap(s)']).any(axis=1)]

def process_data():
   _data = pd.DataFrame()
   _turbo_data = pd.DataFrame()
   column_names = ["hostname", "playbook_id", "task_name", "duration"]

   full_list = os.listdir(path)
   final_list = [nm for nm in full_list if 'results-' in nm]
   for p in final_list:
      objects_no = p.split('-')[1]
      for filename in glob.glob(os.path.join(path+p, '*.csv')):
         _text=pd.read_csv(filename, header=0).reindex(columns=column_names)
         _text = filter_data(_text, objects_no)
         _text['objects_no'] = int(objects_no)
         if 'turbo' in filename:
            _text['turbo'] = 1
            _turbo_data = _turbo_data.append(_text, ignore_index = True)
         else:
            _text['turbo'] = 0
            _data = _data.append(_text, ignore_index = True)

   data = pd.concat([_data, _turbo_data], axis=0)
   data = data.drop('playbook_id', 1)
   data['duration'] = data['duration'].apply(lambda x: pd.Timedelta(x).total_seconds())
   
   df_ns = data[data['task_name'].str.contains('namespace')]
   df_cfm = data[data['task_name'].str.contains('ConfigMap')]

   plot(df_ns, 'Namespace', ['crimson', 'dodgerblue'])
   plot(df_cfm, 'ConfigMap', ['forestgreen', 'darkorange'])

process_data()
