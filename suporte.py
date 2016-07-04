def printDic(k, v):
    for i in range(0, len(k)):
        print k[i]+"\t"+v[i]

def readInputFile(arq):
    
    a = open(arq, "r")
    linhas = a.readlines()
    
    i = 0
    while (i < len(linhas)):
        if(linhas[i][0] == '#'):#remocao das linhas com # no inicio
            linhas.remove(linhas[i])
            i = i - 1 #decrementa o indexador para que o item seguinte ao removido nao seja ignorado
        i = i+1
    
    chaves = []
    valores = []

    for l in linhas:
        ls = l.split('\t')#divide a linha pelia tabulacao
        chave = ls[0]
        valor = '\t'.join(ls[1:])
        if chave in chaves:# caso a chave ja exista  na lista de chaves, seu valor e atualizado sem adicao de nova chave
            valores[chaves.index(chave)] = valor[0:100]
             
        else: #adiciona chave e valor as  respectivas listas
            chaves.append(chave[0:20])
            valores.append(valor[0:100])

    a.close()
    return chaves, valores

