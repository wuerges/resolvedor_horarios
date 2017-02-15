from pulp import *




# Inteiros representado as fases do curso podem ter varias fases. 
# Curso noturnos e diurnos contam como fases separada. 
# Neste caso, como exemplo, estamos considerando as fases de 0-4 
# como sendo do diurno e 5-8 como sendo do noturno
fases = list(range(9))

# cada elemento da lista dos horários é uma fatia do tempo da semana
# cada elemento possui dois inteiros. 
# O primeiro inteiro representa uma das 14 horas do dia:
#   0-4 da manha, 5-9 da tarde e 10-13 da noite.
# O segundo inteiro representa o dia da semana, de 0-4.
horarios = list((h, d) for h in range(14) for d in range(5))

# Cada inteiro da lista profs representa um professor
profs = list(range(2))

# Os turnos são representados por 0 matutino, 1 tarde, 2 noite.
turnos = list(range(3)) #M, V, N


# as CCRs ofertadas são representadas por um dicionário.
# A chave do dicionário é no formato (p, f, t) onde: 
# - p é um professor
# - f é uma fase
# - t é um turno
# O valor é a quantidade de aulas do CCR na semana.
ccrs = { (0, 1, 0): 10 \
       , (0, 2, 0): 10 \
       , (0, 3, 2): 8  \
       }  

# representa o problema ILP
prob = LpProblem("P",LpMaximize)

# armazena as variáveis do problema
# as variáveis são identificadas por uma tupla (p, f, h) onde:
# - p é um professor
# - f é uma fase
# - h é um horário
vs = {}
for f in fases:
    for h in horarios:
        for p in profs:
            vs[(p, f, h)] = LpVariable((p,f, h), 0, 1, LpInteger)

# Adiciona a função objetivo. 
# Neste caso, todas as variáveis são maximizadas.
prob += lpSum(vs.values())

# O mesmo professor não pode estar em mais de um horário ao mesmo tempo.
for h in horarios:
    prob += lpSum(vs[(p, f, h)] for f in fases for p in profs) <= 1, ("time space law for %d %s" % (p, str(h)))


# O a mesma fase e o mesmo turno nao podem estar em mais de um lugar ao mesmo tempo.

for f in fases:
    for h in horarios:
        prob += lpSum(vs[(p, f, h)] for p in profs) <= 1

# Adicionando a contraint de que os turnos das CCRs precisam ser ocupados.
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

