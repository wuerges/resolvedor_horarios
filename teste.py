from pulp import *


fases = list(range(10))
horarios = list((h, d) for h in range(14) for d in range(5))
profs = list(range(2))

turnos = list(range(3)) #M, V, N

ccrs = { (0, 1, 0): 5 }  # (P, F, T): Carga

prob = LpProblem("P",LpMaximize)

vs = {}

for f in fases:
    for h in horarios:
        for p in profs:
            vs[(p, f, h)] = LpVariable((p,f, h), 0, 1, LpInteger)

# adding objective function
prob += lpSum(vs.values())

# same professsor can't be in more than 1 place
for p in profs:
    for h in horarios:
        prob += lpSum(vs[(p, f, h)] for f in fases) <= 1, ("time constraint for %d %s" % (p, str(h)))


# adding maximum time for ccrs
for p in profs:
    for f in fases:
        for t in turnos:
            ch = ccrs.get((p,f,t))
            if not ch:
                ch = 0
            if t == 0:
                prob += lpSum(vs[(p, f, (h, d))] for h in range(0,5) for d in range(5)) == ch
            elif t == 1:
                prob += lpSum(vs[(p, f, (h, d))] for h in range(5,10) for d in range(5)) == ch
            else:
                prob += lpSum(vs[(p, f, (h, d))] for h in range(10,14) for d in range(5)) == ch

prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)

