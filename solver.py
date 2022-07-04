from z3 import *
from itertools import combinations

def printgrid(model,lits):
    grid=[]
    for i in range(9):
        grid+=[[]]
        for j in range(9):
            digit=0
            for dig in range(9):
                if model.evaluate(lits[i][j][dig]):
                    digit=dig+1
                    break
            grid[i]+=[digit]
    for row in grid:
        print(row)

def exactly_one_is_true(literals):
    c=[]
    for pair in combinations(literals,2):
        a,b=pair[0],pair[1]
        c+=[Or(Not(a),Not(b))]
    c+=[Or(literals)]
    return And(c)

def solve(grid):
    lits=[]
    for i in range(9):
        lits+=[[]]
        for j in range(9):
            lits[i]+=[[]]
            for digs in range (9):
                lits[i][j]+=[Bool("x_%i_%i_%i"%(i,j,digs))]

    s=Solver()

    for i in range(9):
        for j in range(9):
            s.add(exactly_one_is_true(lits[i][j]))

    for i in range(9):
        for dig in range(9):
            row=[]
            for j in range(9):
                row+=[lits[i][j][dig]]
            s.add(exactly_one_is_true(row))

    for j in range(9):
        for dig in range(9):
            col=[]
            for i in range(9):
                col+=[lits[i][j][dig]]
            s.add(exactly_one_is_true(col))

    for i in range(3):
        for j in range(3):
            for dig in range(9):
                subgrid=[]
                for x in range(3):
                    for y in range(3):
                        subgrid+=[lits[3*i+x][3*y+j][dig]]
                s.add(exactly_one_is_true(subgrid))
    
    for i in range(9):
        for j in range(9):
            if(grid[i][j]>0):
                s.add(lits[i][j][grid[i][j]-1])
    
    if(str(s.check())=='sat'):
        printgrid(s.model(),lits)
    else:
        print('unsat')

def main():
    file='input.txt'
    grid=[]
    with open(file,'r') as f:
        for line in f.readlines():
            grid.append([int(x) for x in line.split()])
    solve(grid) 


main()