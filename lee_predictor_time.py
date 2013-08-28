'''
Created on Aug 26, 2013

@author: Siviero
'''
import math
from operator import itemgetter, attrgetter
from numpy import *
import scipy as Sci
import scipy.linalg

from general_functions import *
from input_data import *

"""
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
"""
def main():
  # 1: Define the universe of discourse
  # Method: Round min and max to thousand
  umin = math.floor(min(alabama_university_time_series)/1000.0) * 1000;
  umax = math.ceil(max(alabama_university_time_series)/1000.0) * 1000;
  universe = (umin,umax);
  print(universe);
  # 2: Partition of universe
  # Method: Dividing in the thousands
  nIter = int((umax-umin)/1000);
  print(nIter);
  u_vectorized = [];
  for i in range(nIter) :
    u_vectorized.append((umin + i*1000,umin + (i+1)*1000));
  print u_vectorized;  
  # 3: Analyse historical data, putting its values in the intervals
  historical_data_fuzzified = [];
  for val in input_time_series:
    historical_data_fuzzified.append(fetch_fuzzy_class(val, u_vectorized));
  print(historical_data_fuzzified);
  # 4: Establish the relations between fuzzy classes
  # In Lee predictor, number of occurrences and their chronological order are relevant,
  # which is why duplicates are not simply removed
  historical_relations_fuzzy = [];
  historical_weights = {};
  for i in range(len(historical_data_fuzzified)-1):
    _pair = (historical_data_fuzzified[i].get('fuzzy_class'),historical_data_fuzzified[i+1].get('fuzzy_class'));    
    historical_weights[_pair] = i;
    historical_relations_fuzzy.append((historical_data_fuzzified[i].get('fuzzy_class'),historical_data_fuzzified[i+1].get('fuzzy_class')));
    
  
  historical_relations_fuzzy = sorted(historical_relations_fuzzy,key = itemgetter(0,1));
  historical_relations_fuzzy_weighted = [(x,float(historical_relations_fuzzy.count(x))) for x in historical_relations_fuzzy];
  historical_relations_fuzzy_weighted = sorted(list(set(historical_relations_fuzzy_weighted)),key = itemgetter(0,1));
  
  # This could be activated, although for Alabama Enrollment time series it decreased
  # the predictor accuracy
  #print historical_relations_fuzzy_weighted;
  #historical_relations_fuzzy_weighted = [(x[0],x[1]+historical_weights[x[0]]) for x in historical_relations_fuzzy_weighted];
  #print historical_relations_fuzzy_weighted;
  #print _teste;
  
  # Implementation of Lee et al. propposed method, as described in
  # 'Modified Weighted for Enrollment Forecasting Based on Fuzzy Time Series'
  # by Muhammad Hisyam Lee, Riswan Efendi & Zuhaimy Ismail
  # in MATEMATIKA, 2009, Volume 25, Number 1, 67–78
  for j in range(len(historical_data_fuzzified[1:])):
    val = historical_data_fuzzified[j];
    
    weight_list = mat([i[1] for i in historical_relations_fuzzy_weighted if(i[0][0] == val.get('fuzzy_class'))]);
    weight_list /= sum(weight_list);
    mid_points = mat([0.5*(u_vectorized[i[0][1]][0] + u_vectorized[i[0][1]][1]) for i in historical_relations_fuzzy_weighted if(i[0][0] == val.get('fuzzy_class'))]);
    f_old = float((weight_list*mid_points.T)[0][0]);
    _tmp = u_vectorized[val.get('fuzzy_class')];
    diff = input_time_series[j] - (0.5*(_tmp[0] + _tmp[1]));
    historical_data_fuzzified[j+1]['forecasted_data'] = f_old + diff;
      
  # Graph Plotting
  plot_comparison_graph(historical_data_fuzzified);
  
  
if __name__ == '__main__':
    main();