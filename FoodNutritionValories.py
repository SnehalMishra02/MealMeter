#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from pulp import * 
import seaborn as sns


# In[3]:


data = pd.read_csv('./Nutrition.csv').drop('Unnamed: 0',axis=1)



# In[4]:




# In[5]:


data = data[['name','serving_size','calories','carbohydrate','total_fat','protein']]
# print(data.info())
# data.head()


# In[6]:


# sns.countplot(data.serving_size)


# In[7]:


data = data.drop('serving_size',axis=1)
# data.info()


# In[8]:


data['carbohydrate'] = np.array([data['carbohydrate'].tolist()[i].split(' ') for i in range(len(data))])[:,0].astype('float')
data['protein'] = np.array([data['protein'].tolist()[i].split(' ') for i in range(len(data))])[:,0].astype('float')
data['total_fat'] = np.array([data['total_fat'].tolist()[i].split('g') for i in range(len(data))])[:,0].astype('float')


# In[9]:


week_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
split_values = np.linspace(0,len(data),8).astype(int)
split_values[-1] = split_values[-1]-1
def random_dataset():
    frac_data = data.sample(frac=1).reset_index().drop('index',axis=1)
    day_data = []
    for s in range(len(split_values)-1):
        day_data.append(frac_data.loc[split_values[s]:split_values[s+1]])
    return dict(zip(week_days,day_data))


# In[10]:


# random_dataset()['Monday']


# In[11]:


def build_nutritional_values(kg,calories):
    protein_calories = kg*4
    res_calories = calories-protein_calories
    carb_calories = calories/2.
    fat_calories = calories-carb_calories-protein_calories
    res = {'Protein Calories':protein_calories,'Carbohydrates Calories':carb_calories,'Fat Calories':fat_calories}
    return res


# In[13]:


# build_nutritional_values(70,3000)


# In[14]:


def extract_gram(table):
    protein_grams = table['Protein Calories']/4.
    carbs_grams = table['Carbohydrates Calories']/4.
    fat_grams = table['Fat Calories']/9.
    res = {'Protein Grams':protein_grams, 'Carbohydrates Grams':carbs_grams,'Fat Grams':fat_grams}
    return res


# In[15]:


# print(extract_gram(build_nutritional_values(70,2000)))


# In[16]:


days_data = random_dataset()
def model(day,kg,calories):
    G = extract_gram(build_nutritional_values(kg,calories))
    E = G['Carbohydrates Grams']
    F = G['Fat Grams']
    P = G['Protein Grams']
    day_data = days_data[day]
    day_data = day_data[day_data.calories!=0]
    food = day_data.name.tolist()
    c  = day_data.calories.tolist()
    x  = pulp.LpVariable.dicts( "x", indices = food, lowBound=0, upBound=1.5, cat='Continuous', indexStart=[] )
    e = day_data.carbohydrate.tolist()
    f = day_data.total_fat.tolist()
    p = day_data.protein.tolist()
    prob  = pulp.LpProblem( "Diet", LpMinimize )
    prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(food))]  )
    prob += pulp.lpSum( [x[food[i]]*e[i] for i in range(len(x)) ] )>=E
    prob += pulp.lpSum( [x[food[i]]*f[i] for i in range(len(x)) ] )>=F
    prob += pulp.lpSum( [x[food[i]]*p[i] for i in range(len(x)) ] )>=P
    prob.solve()
    variables = []
    values = []
    for v in prob.variables():
        variable = v.name
        value = v.varValue
        variables.append(variable)
        values.append(value)
    values = np.array(values).round(2).astype(float)
    sol = pd.DataFrame(np.array([food,values]).T, columns = ['Food','Quantity'])
    sol['Quantity'] = sol.Quantity.astype(float)
    sol = sol[sol['Quantity']!=0.0]
    sol.Quantity = sol.Quantity/100
    sol = sol.rename(columns={'Quantity':'Quantity (g)'})
    return sol


# In[17]:


def model(prob,day,kg,calories):
    G = extract_gram(build_nutritional_values(kg,calories))
    E = G['Carbohydrates Grams']
    F = G['Fat Grams']
    P = G['Protein Grams']
    day_data = days_data[day]
    day_data = day_data[day_data.calories!=0]
    food = day_data.name.tolist()
    c  = day_data.calories.tolist()
    x  = pulp.LpVariable.dicts( "x", indices = food, lowBound=0, upBound=1.5, cat='Continuous', indexStart=[] )
    e = day_data.carbohydrate.tolist()
    f = day_data.total_fat.tolist()
    p = day_data.protein.tolist()
#    prob  = pulp.LpProblem( "Diet", LpMinimize )
    prob += pulp.lpSum( [x[food[i]]*c[i] for i in range(len(food))]  )
    prob += pulp.lpSum( [x[food[i]]*e[i] for i in range(len(x)) ] )>=E
    prob += pulp.lpSum( [x[food[i]]*f[i] for i in range(len(x)) ] )>=F
    prob += pulp.lpSum( [x[food[i]]*p[i] for i in range(len(x)) ] )>=P
    prob.solve()
    variables = []
    values = []
    for v in prob.variables():
        variable = v.name
        value = v.varValue
        variables.append(variable)
        values.append(value)
    values = np.array(values).round(2).astype(float)
    sol = pd.DataFrame(np.array([food,values]).T, columns = ['Food','Quantity'])
    sol['Quantity'] = sol.Quantity.astype(float)
    sol = sol[sol['Quantity']!=0.0]
    sol.Quantity = sol.Quantity*100
    sol = sol.rename(columns={'Quantity':'Quantity (g)'})
    return sol

    
def total_model(kg,calories):
    result = []
    for day in week_days:
        prob  = pulp.LpProblem( "Diet", LpMinimize )
        print('Building a model for day %s \n'%(day))
        result.append(model(prob,day,kg,calories))
    return dict(zip(week_days,result))


# In[18]:


# diet = total_model(70,3000)


# In[19]:


# diet


# In[ ]:




