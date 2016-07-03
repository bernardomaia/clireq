def lerArquivo(arq):
    
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
        chave, valor = l.split('\t')#divide a linha pela tabulacao

        if chave in chaves:# caso a chave ja exista  na lista de chaves, seu valor e atualizado sem adicao de nova chave
            valores[chaves.index(chave)] = valor 
            if len(valor) > 100:# corta parte do valor caso seu tamanho exceda 100 caracteres
                valores[chaves.index(chave)] = valor[0:100] 
            else:
                valores[chaves.index(chave)] = valor 
        else: #adiciona chave e valor as  respectivas listas
            if len(chave) > 20 :# corta parte da chave caso seu tamanho exceda 20 caracteres
                chaves.append(chave[0:20])
            else:
                chaves.append(chave)

            if len(valor) > 100:# trunca parte do valor caso seu tamanho exceda 100 caracteres
                valores.append(valor[0:100])
            else:
                valores.append(valor)

    a.close()
    return chaves, valores
