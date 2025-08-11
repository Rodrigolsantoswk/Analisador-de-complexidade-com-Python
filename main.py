import os
import sys


def contar_operacoes(line):
    operadores = ['+', '-', '*', '/', '==', '!=', '<=', '>=', '<', '>']
    palavras_chave = ['return', 'print', 'pass', 'break', 'continue']
    if any(op in line for op in operadores):
        return 1
    line_strip = line.strip()
    if any(line_strip.startswith(p) for p in palavras_chave):
        return 1
    return 0


def calculadoraDeComplexidade(
    total_recursoes,
    profundidadeMax,
    temCondicional,
    repet,
    oper,
    dividirParaConquistar=False,
    temParticionamento=False,
    pivotFixado=False
):
    pior = melhor = "O(1)"
    custo_total = f"{oper}"

    if dividirParaConquistar and temParticionamento and total_recursoes >= 2:
        if pivotFixado:
            pior = "O(n^2)"
            melhor = "O(n log n)"
            custo_total = f"n log n + {oper}"
        else:
            pior = "O(n log n)"
            melhor = "O(n log n)"
            custo_total = f"n log n + {oper}"
    elif total_recursoes >= 2:
        pior = "O(2^n)"
        melhor = "O(1)"
        custo_total = f"2^n + {oper}"
    elif total_recursoes == 1:
        if repet == 0:
            pior = melhor = "O(n)"
            custo_total = f"n + {oper}"
        else:
            expo = max(2, profundidadeMax + 1)
            pior = melhor = f"O(n^{expo})"
            custo_total = f"{repet}n^{expo} + {oper}"
    elif profundidadeMax > 0:
        if profundidadeMax > 1:
            pior = f"O(n^{profundidadeMax})"
            melhor = "O(n)" if temCondicional else f"O(n^{profundidadeMax})"
            custo_total = f"{repet}n^{profundidadeMax} + {oper}"
        else:
            pior = "O(n)"
            melhor = "O(1)" if temCondicional else "O(n)"
            custo_total = f"{repet}n + {oper}"

    bigTheta = pior if pior == melhor else "Θ(?)"
    return pior, melhor, custo_total, bigTheta


def analisador(lines):
    loopCont = ifCont = functionCont = 0
    profundidadeMax = profundidadeAtual = oper = repet = 0
    temCondicional = False
    dentroDaFuncao = False
    nomeDaFuncaoAtual = None
    totalRecursoes = 0
    indentFuncao = 0

    temCompreensaoLista = False
    temSlicing = False
    temAtribuicaoPivo = False
    usaComparacaoPivo = False

    for line in lines:
        line_strip = line.strip()

        if not line_strip.startswith(('for', 'while')):
            oper += contar_operacoes(line_strip)

        if line_strip.startswith("def "):
            functionCont += 1
            nomeDaFuncaoAtual = line_strip.split("def ")[1].split("(")[0]
            dentroDaFuncao = True
            totalRecursoes = 0
            indentFuncao = len(line) - len(line.lstrip())
            continue

        if dentroDaFuncao and line.strip() and (len(line) - len(line.lstrip()) <= indentFuncao):
            dentroDaFuncao = False

        if dentroDaFuncao and nomeDaFuncaoAtual and f"{nomeDaFuncaoAtual}(" in line_strip:
            totalRecursoes += line_strip.count(f"{nomeDaFuncaoAtual}(")

        if line_strip.startswith(("for", "while")):
            loopCont += 1
            profundidadeAtual += 1
            profundidadeMax = max(profundidadeMax, profundidadeAtual)
            repet += 1

        if line_strip.startswith("if"):
            ifCont += 1
            temCondicional = True

        if "[" in line_strip and "for" in line_strip and " in " in line_strip and "]" in line_strip:
            temCompreensaoLista = True
        if "[" in line_strip and ":" in line_strip and "]" in line_strip:
            temSlicing = True
        if "pivot" in line_strip and "=" in line_strip and "arr[0]" in line_strip.replace(" ", ""):
            temAtribuicaoPivo = True
        if ("<= pivot" in line_strip) or ("> pivot" in line_strip):
            usaComparacaoPivo = True

        if line_strip == "" or line_strip.startswith("pass") or line_strip.startswith("return"):
            profundidadeAtual = max(0, profundidadeAtual - 1)

    dividirParaConquistar = (totalRecursoes >= 2) and (temCompreensaoLista or temSlicing)
    temParticionamento = (temCompreensaoLista or temSlicing)
    pivotFixado = (temAtribuicaoPivo and usaComparacaoPivo)

    piorCaso, melhorCaso, custo_total, bigTheta = calculadoraDeComplexidade(
        total_recursoes=totalRecursoes,
        profundidadeMax=profundidadeMax,
        temCondicional=temCondicional,
        repet=repet,
        oper=oper,
        dividirParaConquistar=dividirParaConquistar,
        temParticionamento=temParticionamento,
        pivotFixado=pivotFixado
    )

    print("Análise do algoritmo em Python:")
    print(f"Quantidade de loops: {loopCont}")
    print(f"Quantidade de condicionais (if): {ifCont}")
    print(f"Quantidade de funções: {functionCont}")
    print(f"Total de chamadas recursivas detectadas: {totalRecursoes}")
    print(f"Complexidade no pior caso: {piorCaso}")
    print(f"Complexidade no melhor caso: {melhorCaso}")

    print("\nAnálise Assintótica:")
    print(f"Custo 1 (operações e comparações): {oper}")
    print(f"Custo N (loops): {repet}")
    print(f"Custo total estimado: {custo_total}")

    print("\nNotação Assintótica:")
    print(f"Big O: {piorCaso}")
    print(f"Big Omega: {melhorCaso}")
    print(f"Big Theta: {bigTheta}")


def main():
    diretorio = sys.argv[1] if len(sys.argv) > 1 else "quickSort.py"
    try:
        if os.path.exists(diretorio):
            with open(diretorio, encoding="utf-8") as f:
                lines = f.readlines()
                analisador(lines)
        else:
            print(f"Arquivo '{diretorio}' não encontrado.")
    except Exception as e:
        print("Erro na execução do analisador:", e)


if __name__ == "__main__":
    main()
