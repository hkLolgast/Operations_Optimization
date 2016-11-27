'''
Created on Nov 9, 2016

@author: Rick
'''

import numpy as np
from pulp import *
import time
import pygame
# from notifier import Notifier
# nf = Notifier()

# np.random.seed(42)
n_clients = 10
c = n_clients
    
M = 1000000
N = range(0,c+2)
N0= range(0,c+1)
Np= range(1,c+2)
C = range(1,c+1)
# pulpTestAll()



class timer:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
#         print(args)
        print("-"*15)
        print("Timer started for function "+self.func.__name__)
        self.t0 = time.time()
        returnValues = self.func(*args, **kwargs)
        print("Function "+self.func.__name__+" took %.3f seconds" % (time.time()-self.t0))
        print("-"*15)
        self.t0 = None
        return returnValues
    
    def currentTime(self):
        if self.t0:
            return time.time()-self.t0
        else:
            print "Timer not started yet."


id = 0
variablesChanged = False
def addVarConstraint(varName, value):
    global variablesChanged
    variablesChanged = True
    global id
    c = LpConstraint()
    c+= eval(varName)
    c.changeRHS(value)
    problem.addConstraint(c,"vc{}".format(id))
    id+=1

@timer
def add_constraints(problem):
    for j in C:
        exec("c2_{}=LpConstraint()".format(j))
        const = eval("c2_"+str(j))
        
        
        for i in N0:
            if i==j:
                continue
            const+=eval("x_{}_{}".format(i,j))
            if j not in Cd:
                continue
            for k in Np:
                if k==i or k==j:
                    continue
                const+=eval("y_{}_{}_{}".format(i,j,k))
        
        const.changeRHS(1)   
        problem.addConstraint(const, "c2_"+str(j)) 
        
    exec("c3=LpConstraint()")
    const = eval("c3")
    const.changeRHS(1)
    for j in Np:
        const+=eval("x_0_{}".format(j))
         
    problem.addConstraint(const,"c3")
    
    exec("c4=LpConstraint()")
    const = eval("c4")
    const.changeRHS(1)
    for i in N0:
        const+=eval("x_{}_{}".format(i,c+1))
    
    problem.addConstraint(const, "c4")
    
    
    for i in C:
        for j in Np:
            if i==j:
                continue
            exec("c5_{}_{}=LpConstraint()".format(i,j))
            const = eval("c5_{}_{}".format(i,j))
#             const.changeRHS((c+2)*(1-eval("x_{}_{}".format(i,j))))
            const.changeRHS(c+2)
            const+=eval("u_{}".format(i))-eval("u_{}".format(j))+1 +(c+2)*eval("x_{}_{}".format(i,j))<=0
            
#             print const
#             if j==2:
            problem.addConstraint(const, "c5_{}_{}".format(i,j))
    
    
    for j in C:
        exec("c6_{}=LpConstraint()".format(j))
        const = eval("c6_{}".format(j))
        for i in N0:
            if i==j:
                continue
            const+=eval("x_{}_{}".format(i,j))
        for k in Np:
            if k==j:
                continue
            const-=eval("x_{}_{}".format(j,k))
        
        problem.addConstraint(const,"c6_{}".format(j))
    
    
    for i in N0:
        exec("c7_{}=LpConstraint(sense=LpConstraintLE)".format(i))
        const = eval("c7_{}".format(i))
        for j in Cd:
            if i==j:
                continue
            for k in Np:
                if k==i or k==j:
                    continue
                const+=eval("y_{}_{}_{}".format(i,j,k))<=0
        
        const.changeRHS(1)
        problem.addConstraint(const,"c7_{}".format(i))
    
    
    for k in Np:
        exec("c8_{}=LpConstraint(sense=LpConstraintLE)".format(k))
        const = eval("c8_{}".format(k))
        
        for i in N0:
            if i==k:
                continue
            for j in Cd:
                if j==i or j==k:
                    continue
                const+=eval("y_{}_{}_{}".format(i,j,k))<=0
        
        const.changeRHS(1)
        problem.addConstraint(const,"c8_{}".format(k))
    
    
    for i in N0:
        for j in Cd:
            if i==j:
                continue
            for k in Np:
                if i==k or j==k:
                    continue
                exec("c9_{}_{}_{}=LpConstraint()".format(i,j,k))
                const = eval("c9_{}_{}_{}".format(i,j,k))
                const+= 2*eval("y_{}_{}_{}".format(i,j,k))<=0
                
                for h in Np:
                    if h==i:
                        continue
                    const-= eval("x_{}_{}".format(i,h))
                
                for l in N0:
                    if l==k:
                        continue
                    const-= eval("x_{}_{}".format(l,k))
                
                problem.addConstraint(const, "c9_{}_{}_{}".format(i,j,k))
        
    
    for i in C:
        exec("c11_{}=LpConstraint()".format(i))
        const1 = eval("c11_{}".format(i))
        const1+= eval("t_d_{}".format(i))>=eval("t_t_{}".format(i))
        const1+= M
        
        exec("c12_{}=LpConstraint()".format(i))
        const2 = eval("c12_{}".format(i))
        const2+= eval("t_t_{}".format(i))>=eval("t_d_{}".format(i))
        const2+= M
        
        for j in Cd:
            if i==j:
                continue
            for k in Np:
                if k==i or k==j:
                    continue
                const1-= M*eval("y_{}_{}_{}".format(i,j,k))
                const2-= M*eval("y_{}_{}_{}".format(i,j,k))
        
        problem.addConstraint(const1, "c11_{}".format(i))
        problem.addConstraint(const2, "c12_{}".format(i))
    
    
    for k in N:
        exec("c13_{}=LpConstraint()".format(k))
        const1 = eval("c13_{}".format(k))
        const1+= eval("t_d_{}".format(k))>=eval("t_t_{}".format(k))
        const1+= M
        
        exec("c14_{}=LpConstraint()".format(k))
        const2 = eval("c14_{}".format(k))
        const2+= eval("t_t_{}".format(k))>=eval("t_d_{}".format(k))
        const2+= M
        
        if k==0:
            problem.addConstraint(const1, "c13_{}".format(k))
            problem.addConstraint(const2, "c14_{}".format(k))
            continue
        
        for i in N0:
            if i==k:
                continue
            for j in Cd:
                if j==i or j==k:
                    continue
                const1-= M*eval("y_{}_{}_{}".format(i,j,k))
                const2-= M*eval("y_{}_{}_{}".format(i,j,k))
    
        problem.addConstraint(const1, "c13_{}".format(k))
        problem.addConstraint(const2, "c14_{}".format(k))
    
    
    for h in N0:
        for k in Np:
            if h==k:
                continue
            exec("c15_{}_{}=LpConstraint()".format(h,k))
            const = eval("c15_{}_{}".format(h,k))
            
            const+=eval("t_t_{}".format(k))>=eval("t_t_{}".format(h))+tau_t[h,k]\
                                -M*(1-eval("x_{}_{}".format(h,k)))
            
            for l in Cd:
                if l==h:
                    continue
                for m in Np:
                    if m==h or m==l:
                        continue
                    const-= SL*eval("y_{}_{}_{}".format(h,l,m))
            
            for i in N0:
                if i==k:
                    continue
                for j in Cd:
                    if j==i or j==k:
                        continue
                    const-= SR*eval("y_{}_{}_{}".format(i,j,k))
            
            problem.addConstraint(const, "c15_{}_{}".format(h,k))
    
    
    for j in Cd:
        for i in N0:
            if i==j:
                continue
            exec("c16_{}_{}=LpConstraint()".format(j,i))
            const = eval("c16_{}_{}".format(j,i))
            
            const+=eval("t_d_{}".format(j))>=eval("t_d_{}".format(i))+tau_d[i,j]+SL-M
            
            for k in Np:
                if k==i or k==j:
                    continue
                const-= M*eval("y_{}_{}_{}".format(i,j,k))
                
            problem.addConstraint(const, "c16_{}_{}".format(j,i))
            
    for j in Cd:
        for k in Np:
            if j==k:
                continue
            exec("c17_{}_{}=LpConstraint()".format(j,k))
            const = eval("c17_{}_{}".format(j,k))
            
            const+=eval("t_d_{}".format(k))>=eval("t_d_{}".format(j))+tau_d[j,k]+SR-M
            
            for i in N0:
                if i==j or i==k:
                    continue
                const-= M*eval("y_{}_{}_{}".format(i,j,k))
                
            problem.addConstraint(const, "c17_{}_{}".format(j,k))
    
    
    for k in Np:
        for i in N0:
            if i==k:
                continue
            exec("c18_{}_{}=LpConstraint()".format(k,i))
            const = eval("c18_{}_{}".format(k,i))
            const+=eval("t_d_{}".format(k))-eval("t_d_{}".format(i))<=E+M
            
            for j in Cd:
                if i==j or j==k:
                    continue
                const+= M*eval("y_{}_{}_{}".format(i,j,k))
                
            problem.addConstraint(const, "c18_{}_{}".format(k,i))
    
    
    for i in C:
        for j in C:
            if i==j:
                continue
            exec("c19_{}_{}=LpConstraint()".format(i,j))
            const = eval("c19_{}_{}".format(i,j))
            const+= eval("u_{}".format(i))-eval("u_{}".format(j))>=1-(c+2)*eval("p_{}_{}".format(i,j))
            
            problem.addConstraint(const,"c19_{}_{}".format(i,j))
            
            exec("c20_{}_{}=LpConstraint()".format(i,j))
            const = eval("c20_{}_{}".format(i,j))
            const+= eval("u_{}".format(i))-eval("u_{}".format(j))<=-1+(c+2)*(1-eval("p_{}_{}".format(i,j)))
            
            problem.addConstraint(const,"c20_{}_{}".format(i,j))
            
            exec("c21_{}_{}=LpConstraint()".format(i,j))
            const = eval("c21_{}_{}".format(i,j))
            const+= eval("p_{0}_{1}+p_{1}_{0}".format(i,j))
            const.changeRHS(1)
            
            problem.addConstraint(const,"c21_{}_{}".format(i,j))
    
    
    for i in N0:
        for k in Np:
            if i==k:
                continue
            for l in C:
                if i==l or l==k:
                    continue
                 
                exec("c22_{}_{}_{}=LpConstraint()".format(i,k,l))
                const = eval("c22_{}_{}_{}".format(i,k,l))
                 
                const+= eval("t_d_{}".format(l))>=eval("t_d_{}".format(k))-3*M+M*eval("p_{}_{}".format(i,l))
                 
                for j in Cd:
                    if j==i or j==k or j==l:
                        continue
                    const-= M*eval("y_{}_{}_{}".format(i,j,k))
                     
                for m in Cd:
                    if m==i or m==k or m==l:
                        continue
                    for n in Np:
                        if n==i or n==k or n==l or n==m:
                            continue
                        const-= M*eval("y_{}_{}_{}".format(l,m,n))
                 
                problem.addConstraint(const,"c22_{}_{}_{}".format(i,k,l))
                
    
    problem.addConstraint(eval("t_t_0")==0,"c23")
    problem.addConstraint(eval("t_d_0")==0,"c24")
    
    for j in C:
        problem.addConstraint(eval("p_0_{}".format(j))==1,"c25_{}".format(j))
         
    for i in Np:
        problem.addConstraint(eval("u_{}".format(i))>=1,"c28_{}_lower".format(i))
        problem.addConstraint(eval("u_{}".format(i))<=c+1,"c28_{}_upper".format(i))
         
    for i in N:
        problem.addConstraint(eval("t_t_{}".format(i))>=0,"c29_{}".format(i))
        problem.addConstraint(eval("t_d_{}".format(i))>=0,"c30_{}".format(i))
    
    for i in C:
        problem.addConstraint(eval("u_{}".format(i))<=eval("u_{}".format(c+1)),"c31_{}".format(i))
    
    for j in F:
        exec("c32_{}=LpConstraint()".format(j))
        const = eval("c32_{}".format(j))
        varName = "z_{}".format(j)
        exec(varName+'=LpVariable("'+varName+'",cat=LpBinary)')
        for i in N0:
            if i==j:
                continue
            const += eval("x_{}_{}".format(i,j))==eval("z_{}".format(j))
        problem.addConstraint(const, "c32_{}".format(j))    
        problem.objective += M*eval("z_{}".format(j))
        
    exec("c33=LpConstraint()")
    const = eval("c33")
    for i in N0:
        for j in Np:
            if i==j:
                continue
            const+=eval("x_{}_{}".format(i,j))*truck_dist[i,j]<=0
    r = LpVariable("r",cat=LpInteger)
    const -= fuel*(r+1)
    
    problem.addConstraint(const, "c33")
    
    problem.objective += 50*r


@timer
def main(problem, print_output=True):
    problem.solve(CPLEX_CMD())
    vars = problem.variables()
    if all(value(v)==None for v in vars):
        raise ValueError,"No solution found"
    if print_output:
        if all(value(v)!=None for v in vars if str(v)!="__dummy"):
            print "Solution found"
            print "Objective: ",value(problem.objective)
        else:
            for v in problem.variables():
                print v, value(v)

def get_distances():
    coords = []
    for i in range(n_clients+1):                                #+1 for depot
        coords.append(np.random.randint(0,2000,size=2))
    raw_dist = np.empty((n_clients+1,n_clients+1))
    for i in range(n_clients+1):
        for j in range(n_clients+1):
            if i==j:
                raw_dist[i,j] = M
            else:
                d = np.linalg.norm(coords[i]-coords[j])
                raw_dist[i,j] = d
    
    truck_dist = np.int32(raw_dist/35)
    truck_dist-= I*truck_dist
    truck_dist+= I*M
    
#     print "AVG truck: {:.2f}".format(np.average(truck_dist-I*M))
    
    drone_dist = np.int32(raw_dist/50)
    drone_dist-= I*drone_dist
    drone_dist+= I*M
    
#     print "AVG drone: {:.2f}".format(np.average(drone_dist-I*M))

    return truck_dist, drone_dist, coords
                 
    

if __name__ == '__main__':
#     seed = 1480256015
    seed = 1480272780
#     seed = int(time.mktime(time.localtime()))
    print "Used seed:",seed
    np.random.seed(seed)
    I = np.eye(1+n_clients)
    get_distances()
    size = (1+n_clients, 1+n_clients)
    
#     truck_dist = np.random.randint(15,25,size=size)
#     drone_dist = truck_dist-np.random.randint(3,10,size=size)
#     
#     drone_dist-= I*drone_dist
#     drone_dist+= I*M
#     
#     truck_dist-= I*truck_dist
#     truck_dist+= I*M
    
    truck_dist, drone_dist, coords = get_distances()
    
    print "Average truck distance: {:.2f}".format(np.average(truck_dist-I*M))
    print "Average drone distance: {:.2f}".format(np.average(drone_dist-I*M))
    
    print "truck distances:", truck_dist
    print "drone distances:", drone_dist
    
    
    truck_dist = np.c_[truck_dist, truck_dist[:,0]]
    
    
#     heavy_parcels = np.random.randint(0,4,size=n_clients)
    parcel_weight = 5*np.random.beta(a=2, b=5, size=n_clients)
    heavy_parcels = parcel_weight>2.3
#     heavy_parcels = np.array([0,1,1,1])
    parcel_sizes  = np.random.randint(50,350,size=(n_clients,3))
    large_parcels = np.any(parcel_sizes>325,axis=1)
    
    signature_required = np.random.randint(0,5, size=n_clients)==0
    
    Cd = C[:]
    for i in range(len(heavy_parcels)):
        if heavy_parcels[i] or large_parcels[i] or signature_required[i]:
            Cd.remove(i+1)
    
    
    validAreas = False
    while not validAreas:
        forbiddenAreas = np.random.randint(0,4,size=n_clients)==0      #Truck can't go there
        for i in range(len(heavy_parcels)):
            if forbiddenAreas[i] and i+1 not in Cd:
                break
        else:
            validAreas = True
#     print forbiddenAreas
    F = [i+1 for i in range(n_clients) if forbiddenAreas[i]]
    
    
    for i in range(n_clients):
        print "Package {:<2}: {:.2f}kg, {:<12} ".format(i+1, parcel_weight[i], "x".join(map(str, parcel_sizes[i]))+"."),
        statuses = []
        if heavy_parcels[i]:
            statuses.append("TOO HEAVY")
        if large_parcels[i]:
            statuses.append("TOO LARGE")
        if signature_required[i]:
            statuses.append("SIGNATURE REQUIRED")
        if forbiddenAreas[i]:
            statuses.append("IN TOLL AREA")
        if not statuses:
            statuses.append("Deliverable by drone and truck")
        print "Status: ", ", ".join(statuses)
    
    
    for i in range(n_clients+1):
        for j in range(i):
            drone_dist[i,j] = drone_dist[j,i] = min(drone_dist[i,j],drone_dist[j,i])               #make symmetric
    
    drone_dist = np.c_[drone_dist, drone_dist[:,0]]
    
#     print truck_dist
#     print
#     print drone_dist
    
    adj_coords = []
    for (x,y) in coords:
        adj_coords.append((x/4+50, y/4+50))
#         
#     screen = pygame.display.set_mode((600,600))
#     screen.fill((255,255,255))
#     
#     for i,(x,y) in enumerate(adj_coords):
#         if i==0:
#             color = (0,0,255)
#         elif i not in Cd:
#             color = (255,0,0)
#         elif i in F:
#             color = (0,0,0)
#         else:
#             color = (0,255,0)
#             
#         pygame.draw.circle(screen, color, (x,y), 5)        
#         
#     pygame.display.flip()
#     
#     quit = False
#     while not quit:
#         event = pygame.event.poll()
#         if event.type==pygame.QUIT:
#             quit = True
#             
#     pygame.display.quit()
            
    #===========================================================================
    # LINEAR PROGRAMMING MODEL
    #===========================================================================
    
    
    problem = LpProblem("FSTSP",LpMinimize)
    tau_t = truck_dist
    tau_d = drone_dist
    SL = 2
    SR = 2
    E = 25
    fuel = 100
    
    for i in N0:
        for j in Np:
            if i==j:
                continue
            varName = "x_{}_{}".format(i,j)
            exec(varName+'=LpVariable("'+varName+'",cat=LpBinary)')
            
            varName = "p_{}_{}".format(i,j)
            exec(varName+'=LpVariable("'+varName+'",cat=LpBinary)')
            
            if j==c+1:
                continue
            if heavy_parcels[j-1]:
                continue
            for k in Np:
                if k==i or k==j:
                    continue
                varName = "y_{}_{}_{}".format(i,j,k)
                exec(varName+'=LpVariable("'+varName+'",cat=LpBinary)')
            
    for j in N:
        varName = "t_t_{}".format(j)
        exec(varName+'=LpVariable("'+varName+'")')
        varName = "t_d_{}".format(j)
        exec(varName+'=LpVariable("'+varName+'")')
        
    for i in Np:
        varName = "u_{}".format(i)
        exec(varName+'=LpVariable("'+varName+'",cat=LpInteger)')
        
    problem+=eval("t_t_{}".format(c+1))
    
    
    add_constraints(problem)
    
    for c in problem.constraints:
        s = str(problem.constraints[c])
        rhs = False
        for part in s.split(" "):
            if "=" in part:
                rhs = True
            assert part.count("*")<=1
            try:
                assert sum(part.count(v) for v in ["x","y","z","p","q","r","t","u"])<=(not rhs)
            except:
                if not "t_t" in part:
                    print "{:<13} {:<20} {}".format(c,part, s)
                    raise
            if "*" in part:
                mult = part[:part.index("*")]
                try:
                    int(mult)
                except:
                    print c, part, mult, s
                    raise
            
    s = str(problem.objective)
    rhs = False
    for part in s.split(" "):
        if "=" in part:
            rhs = True
        assert part.count("*")<=1
        try:
            assert sum(part.count(v) for v in ["x","y","z","p","q","r","t","u"])<=(not rhs)
        except:
            if not "t_t" in part:
                print "{:<20} {}".format(part, s)
                raise
        if "*" in part:
            mult = part[:part.index("*")]
            try:
                int(mult)
            except:
                print part, mult, s
                raise
    
    
        
    disabledConstraints = []
    removedConstraints = []
    for co in problem.constraints:
        for dis in disabledConstraints:
            if co.startswith("c{}_".format(dis)) or co=="c{}".format(dis):
                removedConstraints.append((problem.constraints[co], co))
                del problem.constraints[co]
    

    print
    print "Solving problem with {} variables...".format(len(problem.variables()))
    seen = set()
    vars = problem.variables()
    for var in vars:
        char = str(var)[0]
        if char in seen:
            continue
        else:
            am = len([v for v in vars if str(v).startswith(char)])
            print "\t{} {} variable{}".format(am, char, "s" if am>1 else "")
            seen.add(char)
    
    addVarConstraint("x_0_2", 1)
    addVarConstraint("x_2_6", 1)
#     addVarConstraint("y_2_6_10", 1)
    addVarConstraint("x_6_10", 1)
    addVarConstraint("x_8_11", 1)
    
#     print min(tau_t[2,10], tau_d[2,6]+tau_d[6,10]), E
#     for i1 in range(6,34):
#         print i1
#         for i2 in range(i1+1,34):
#             if i1==i2:
#                 continue
#             for i3 in range(i2+1, 34):
#                 disabledConstraints = []
#     #             index = i1
#                 for index in (i1,i2,i3):
#                     for co in problem.constraints:
#                         if co.startswith("c{}_".format(index)) or co=="c{}".format(index):
#                             disabledConstraints.append((problem.constraints[co],co))
#                             del problem.constraints[co]
#                          
#                 if not disabledConstraints:
#                     continue
#                 try:
#     #                 print "{} constraints".format(len(problem.constraints))
#                     main(problem, print_output=False)
#                 except ValueError:
#         #             print "Removing constraint {} ({} occurences) has no effect".format(index, len(disabledConstraints))
#                     pass
#                 else:
#                     print "FIX: Removing constraint {}, {} and {} gives a solution".format(i1, i2, i3)
#                     quit()
#                 for (co,name) in disabledConstraints:
#                     problem.addConstraint(co, name)
#     quit()
    
    problem.writeLP("C:\\Users\\Rick\\opl\\opsopt\\fstsp.lp")
    
#     for co in problem.constraints:
#         if co.startswith("c5"):
#             print co, problem.constraints[co],",", value(problem.constraints[co])

    main(problem)
    
#     nf.notify("Solver done")
    
    if not variablesChanged:
        f = open("variables.txt","w")
        f.write(str(seed)+"\n")
        for v in vars:
            f.write("{:<10} {}\n".format(str(v), value(v)))
        f.close()
    
    if removedConstraints:
        print "Removed constraints status:"
        for (co, name) in removedConstraints:
            problem.addConstraint(co, name)
            print name, co, value(co)
    
    print
#     print "-"*50
#     for v in vars:
#         if str(v).startswith("x") and round(value(v))==1:
#             print v
#           
#         if str(v).startswith("y") and round(value(v))==1:
#             print v
#             
    print    
    
    done = False
    newIndex = "0"
    while not done:
#         print "new:",newIndex
        x = [v for v in vars if str(v).startswith("x_{}_".format(newIndex)) and round(value(v))==1][0]
        deps = [v for v in vars if str(v).startswith("y_{}_".format(newIndex)) and round(value(v))==1]
        arrivs = [v for v in vars if str(v).startswith("y") and str(v).endswith("_{}".format(newIndex)) and round(value(v))==1]
        assert len(deps)<=1 and len(arrivs)<=1
#         print x,
#         if arrivs:
#             print "<- {}".format(arrivs[0]),
#             if deps:
#                 print ", ",
#         if deps:
#             print "-> {}".format(deps[0]),
#         print
        if arrivs:
            ar = arrivs[0]
        if deps:
            dep = deps[0]
            
        print "{:<8} {:<13} {:<15}".format(x, "<- {}".format(ar) if arrivs else "", "-> {}".format(dep) if deps else "")
        for usc in range(len(str(x))-1,-1,-1):
            if str(x)[usc]=="_":
                break
        newIndex = str(x)[usc+1:]
        if newIndex==str(n_clients+1):
            done = True
            depotArrivs = [v for v in vars if str(v).startswith("y") and str(v).endswith("_{}".format(newIndex)) and round(value(v))==1]
            if depotArrivs:
                print "{:<8} {:<13}".format("","<- {}".format(depotArrivs[0]))
    
    screen = pygame.display.set_mode((600,600))
    screen.fill((255,255,255))
    
    for i,(x,y) in enumerate(adj_coords):
        if i==0:
            c = (0,0,255)
        elif i not in Cd:
            c = (255,0,0)
        elif i in F:
            c = (0,0,0)
        else:
            c = (0,255,0)
            
        pygame.draw.circle(screen, c, (x,y), 5)       
    
    for v in vars:
        if (str(v).startswith("x") or str(v).startswith("y")) and round(value(v))==1:
            s = str(v)
            usc1 = s.find("_")
            usc2 = s.find("_",usc1+1)
            usc3 = s.find("_",usc2+1)
            
            i = int(s[usc1+1:usc2])
            j = int(s[usc2+1:(usc3 if usc3!=-1 else 100)])%(n_clients+1)                 #c+1==depot==0
            
            c = (0,0,0) if str(v).startswith("x") else (0,0,255)
            
            x1,y1 = adj_coords[i]
            x2,y2 = adj_coords[j]
            
            pygame.draw.line(screen, c, (x1,y1),(x2,y2))
            
            if str(v).startswith("y"):
                k = int(s[usc3+1:])%(n_clients+1)                 #c+2==depot==0
                x3,y3 = adj_coords[k]
                pygame.draw.line(screen, c, (x2,y2),(x3,y3))
                
    
    pygame.display.flip()
    
    quit = False
    while not quit:
        event = pygame.event.poll()
        if event.type==pygame.QUIT:
            quit = True
            
    