'''
Created on Aug 27, 2013

@author: Siviero
'''
import matplotlib.pyplot as plt

def fetch_fuzzy_class(val,u_v):
  for u_min,u_max in u_v:
    if(val >= u_min and val <= u_max):
      dict_object = {'actual_data' : val, 'fuzzy_class' : u_v.index((u_min,u_max))};
      return dict_object;

def fetch_fuzzy_relations(val,fuzzy_relation_vector):
  r_list = []
  for i in range(len(fuzzy_relation_vector)):
    if(fuzzy_relation_vector[i][0] == val):
      print fuzzy_relation_vector[i];
      r_list.append(fuzzy_relation_vector[i]);
  return r_list;       

def get_midpoint(tuple):
  return 0.5*(tuple[0]+tuple[1]);

def plot_comparison_graph(historical_data_forecasted):
  actual = [x.get('actual_data') for x in historical_data_forecasted[1:]];
  predicted = [x.get('forecasted_data') for x in historical_data_forecasted[1:]];
  
  #print actual;
  #print predicted;
  plt.plot(range(len(actual)),actual,'r',range(len(actual)),predicted,'b');
  plt.show();