''
Created on Oct. 5, 2021

@author: theone
'''
import sys 
from copy import deepcopy

assign_true = set()
assign_false = set()
n_props, n_splits = 0, 0

#------------------------------  

def solve(rows,literals):
    global assign_true, assign_false, n_props, n_splits
    
    new_true = []
    new_false = []
    n_splits += 1
    
    rows = rows
    
    units=[] #[['1']] a unit clause with just 1 variable 
    for i in rows: #compare to: units=[i for i in rows if len(i)==1], only keep the content of each unit clause 
        if len(i)==1:
            units.append(i[0])

    if len(units): #if exit unit clause 
        for unit in units: #for each unit clause 
            n_props += 1
            if '-' in unit: #if the clause is "-4", append 4 to assign false 
                assign_false.add(unit[1:])
                new_false.append(unit[1:])
                i=0
                while True:
                    if unit in rows[i]: #if a clause contains "-4", remove the clause 
                        rows.pop(i) 
                        i -= 1
                    elif unit[1:] in rows[i]: #if a clause contains "4", remove this literal
                        rows[i].remove(unit[1:])
                    i += 1
                    if i >= len(rows):
                        break
            else: #unit clause of positive literal 
                assign_true.add(unit)
                new_true.append(unit)
                i = 0
                while True:
                    if "-"+unit in rows[i]: #if a clause contains "-4", remove the literal 
                        rows[i].remove("-"+unit)
                    elif unit[0] in rows[i]: #if a clause contains "4", remove this clause
                        rows.pop(i)
                        i -= 1
                    i += 1
                    if i >= len(rows):
                        break

    print('Units =', units)
    print('CNF after unit propogation = ', end = '')
    print(rows)
    
    if len(rows) == 0:
        return True
    
    if sum(len(clause)==0 for clause in rows):
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        print('Null clause found, backtracking...')
        return False 
        
    literals=set()
    for r in rows:
        for variable in r:
            if variable[0].isdigit(): #"13"
                literals.add(variable)
            else:
                literals.add(variable[1:])
    
    print("literals are:",literals)
    x = list(literals)[0]
    print("x is: ",x)
    newrows=deepcopy(rows)
    #print("new row is: ", newrows)
    newrows.append([x])
    print("new row is: ", newrows)
    print("------------- call solve again ---------------")
    #sys.exit()
    if solve(newrows, deepcopy(literals)): #assign x is true by adding unit clause [x]
        return True
    elif solve(deepcopy(rows).append(['-'+x]), deepcopy(literals)):
        return True
    else:
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        return False
 
   
input_cnf = open("test.txt", 'r').read()
cnf = input_cnf.splitlines() #list of all the rows 
cnf=list(set(cnf))
TotalRows=[]
TotalLiterals=set()
for row in cnf:
    r=row.split() # ["-1"," "," ", "13"]
    r=[i for i in r if i] #get rid of the spaces  
    if len(r)>0 and not r[0][0].isalpha(): #get rid of this row: ["c"," "," ", "quinn"]
        TotalRows.append(r)
        for variable in r:
            if variable[0].isdigit(): #"13"
                TotalLiterals.add(variable)
            else:
                TotalLiterals.add(variable[1:]) #if start with "-", add the remaining 

print("all cnf:")
print(TotalRows)
print("all literals:")
print(TotalLiterals) 

if solve(TotalRows,TotalLiterals):
    print('\nResult: SATISFIABLE')
    print('\nNumber of Splits =', n_splits)
    print('Unit Propogations =', n_props)
    print('Solution:')
    for i in assign_true:
        print('\t\t'+i, '= True')
    for i in assign_false:
        print('\t\t'+i, '= False')
else:
    print("reached root")
    print('\nResult: UNSATISFIABLE')
    print('Number of Splits =', n_splits)
    print('Unit Propogations =', n_props)
    print()

