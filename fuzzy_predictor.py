'''
Created on Aug 26, 2013

@author: Siviero
'''
import math
from operator import itemgetter, attrgetter
alabama_university_time_series = [13055,13563,13867,14696,15460,15311,15603,
                                  15861,16807,16919,16388,15433,15497,15145,
                                  15163,15984,16859,18150,18970,19328,19337,
                                  18876];

def fetch_fuzzy_class(val,u_v):
  for u_min,u_max in u_v:
    if(val >= u_min and val <= u_max):
      dict_object = {'actual_data' : val, 'fuzzy_class' : u_v.index((u_min,u_max))};
      return dict_object;
      

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
  for val in alabama_university_time_series:
    historical_data_fuzzified.append(fetch_fuzzy_class(val, u_vectorized));
  print(historical_data_fuzzified);
  # 4: Establish the relations between fuzzy classes
  # First, generates a list of relations, then use a set to remove duplicates
  historical_relations_fuzzy = [];
  for i in range(len(historical_data_fuzzified)-1):
    #a= (historical_data_fuzzified[i].get('fuzzy_class'),historical_data_fuzzified[i+1].get('fuzzy_class'));
    historical_relations_fuzzy.append((historical_data_fuzzified[i].get('fuzzy_class'),historical_data_fuzzified[i+1].get('fuzzy_class')));
  historical_relations_fuzzy = sorted(list(set(historical_relations_fuzzy)),key = itemgetter(0,1));
  print historical_relations_fuzzy;
  # for k = 3:n
  print historical_data_fuzzified[2:]; 
if __name__ == '__main__':
    main();