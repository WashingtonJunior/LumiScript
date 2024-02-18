import sys
import os

if len(sys.argv)>1:
    localfile = sys.argv[1]
else:
    localfile = "GrootTest.gcode"


arq = localfile
arq2 = localfile.replace("Test", "Test2")
#print(arq)
#print(arq2)

#arq = "d:/temp/TesteUnicornio/Unicornio1.gcode"
#arq2 = "d:/temp/TesteUnicornio/xUnicornio2.gcode"

f = open(arq, encoding="utf-8")

#linhas = []

#for i in range(550615):
#    print(i)
#    linhas.append(f.readline())


linhas = f.readlines()
#cmdp = ["M600\n", "PAUSE\n", "M25\n", "M0\n"]
cmdp = ["M600", "PAUSE", "M25", "M0"]

preCode = []

for idx in range(len(linhas)):
    if linhas[idx]=="T0\n":
        ultimo = idx
        print("Precode: " + str(ultimo))
        break
    else:
        preCode.append(linhas[idx])

linhas = linhas[ultimo:]

qtT = 0
for idx in range(len(linhas)):
    if linhas[idx].startswith("T") and linhas[idx].endswith("\n"):
        try:
            n = int(linhas[idx].replace("T", "").replace("\n", ""))
        except Exception:
            n = -1

        if n>qtT:
            qtT = n

print("#T: " + str(qtT))
#input()

TG = []

for t in range(qtT+2):
    TG.append([])
    insere = False
    for idx in range(len(linhas)):
        if linhas[idx]=="T" + str(t) + "\n":
            insere = True
            TG[t].append(linhas[idx])
            #print(linhas[idx])
        # elif linhas[idx].replace(" ", "") in cmdp:
        #     insere = False
        #     cmdpUsado = linhas[idx].replace(" ", "")
        elif linhas[idx].strip().split(" ")[0] in cmdp:
            insere = False
            #cmdpUsado = linhas[idx].replace(" ", "")
            cmdpUsado = linhas[idx].strip()
            #print(linhas[idx], cmdpUsado)
        else:
            if insere:
                TG[t].append(linhas[idx])
    if len(TG[t])>0:
        print("T" + str(t) + " processed!")


for iG in range(len(TG)):
    G = TG[iG]
    cpRemoveStart = -1
    cpRemoveEnd = -1

    if len(G)>0:
        iLinha = 0
        while iLinha < len(G):
            if G[iLinha].startswith("; CP TOOLCHANGE END"): 
                cpRemoveEnd = iLinha
            if G[iLinha].startswith("; CP TOOLCHANGE START"):
                cpRemoveStart = iLinha

            if cpRemoveStart>-1 and cpRemoveEnd>-1:
                #print("cpRemoveStart", cpRemoveStart)
                #print("cpRemoveEnd", cpRemoveEnd)
                #input()

                if cpRemoveEnd>cpRemoveStart:
                    #if iG==0:
                    #    print(G[cpRemoveStart:cpRemoveEnd])
                    chunk = G[cpRemoveStart:cpRemoveEnd]
                    temZ = [el for el in chunk if el.startswith("G1 Z")]
                    #if temZ:
                    #    print("tem")
                    #else:
                    #    print("ntem")
                    #print(temZ)
                    #input()
                    #print(chunk)
                    #input()

                    # if temZ:
                    #     print(G[cpRemoveStart:cpRemoveEnd])
                    #     cpRemoveEnd = -1
                    #     cpRemoveStart = -1
                    #     pass
                    # else:
                    G = G[:cpRemoveStart] + temZ + G[cpRemoveEnd:]
                    TG[iG] = G
                    cpRemoveEnd = -1
                    cpRemoveStart = -1
                    iLinha = 0
                    #print("removeu")
                    #input()

            iLinha += 1

        #f2 = open('d:/temp/T' + str(iG) + ".txt", 'w')
        #f2.writelines(G)
        #f2.close()        

        #input()


f.close()

print("Writing to '" + arq2 + "'...")

f2 = open(arq2, 'w')

f2.writelines(preCode)

for iG in range(qtT+1):
    G = TG[iG]
    if len(G)>0:
        f2.writelines(G)

        if len(TG[iG+1])>0:
            f2.write(cmdpUsado.replace("\n", "") + " ; LumiScript\n")

print("Done!")

f2.close()
