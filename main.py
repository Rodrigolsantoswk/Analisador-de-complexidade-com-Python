import os


def contar_operacoes(line):
    operadores = ['+', '-', '*', '/', '==', '!=', '<=', '>=', '<', '>']
    palavras_chave = ['return', 'print', 'pass', 'break', 'continue']

    if any(op in line for op in operadores):
        return 1

    line_strip = line.strip()
    if any(line_strip.startswith(pal) for pal in palavras_chave):
        return 1

    return 0


def calculadoraDeComplexidade(recursoes, profundidadeMax, temCondicional, repet, oper):
    if recursoes > 1:
        pior = melhor = "O(2^n)"
        custo_total = f"2^n + {oper}"
    elif recursoes == 1:
        pior = melhor = "O(n)"
        custo_total = f"n + {oper}"
    elif profundidadeMax > 0:
        pior = f"O(n^{profundidadeMax})"
        melhor = "O(1)" if temCondicional and profundidadeMax == 1 else "O(n)"
        if profundidadeMax > 1:
            custo_total = f"{repet}n^{profundidadeMax} + {oper}"
        else:
            custo_total = f"{repet}n + {oper}"
    else:
        pior = melhor = "O(1)"
        custo_total = f"{oper}"

    bigTheta = pior if pior == melhor else "Θ(?)"
    return pior, melhor, custo_total, bigTheta


def analisador(lines):
    loopCont = ifCont = functionCont = recursoesNaLinha = 0
    profundidadeMax = profundidadeAtual = oper = repet = 0
    temCondicional = False
    dentroDaFuncao = False
    nomeDaFuncaoAtual = None

    for line in lines:
        line_strip = line.strip()

        if not line_strip.startswith(('for', 'while')):
            oper += contar_operacoes(line_strip)

        if line_strip.startswith("def "):
            functionCont += 1
            nomeDaFuncaoAtual = line_strip.split("def ")[1].split("(")[0]
            dentroDaFuncao = True

        if dentroDaFuncao and not line_strip.startswith("def "):
            chamadas = line_strip.count(f"{nomeDaFuncaoAtual}(")
            if chamadas > 0:
                recursoesNaLinha = max(recursoesNaLinha, chamadas)

        if line_strip.startswith(("for", "while")):
            loopCont += 1
            profundidadeAtual += 1
            profundidadeMax = max(profundidadeMax, profundidadeAtual)
            repet += 1

        if line_strip.startswith("if"):
            ifCont += 1
            temCondicional = True

        if line_strip == "" or line_strip.startswith("pass"):
            dentroDaFuncao = False
            profundidadeAtual = max(0, profundidadeAtual - 1)

    piorCaso, melhorCaso, custo_total, bigTheta = calculadoraDeComplexidade(
        recursoesNaLinha, profundidadeMax, temCondicional, repet, oper
    )

    print("Análise do algoritmo em Python:")
    print(f"Quantidade de loops: {loopCont}")
    print(f"Quantidade de condicionais (if): {ifCont}")
    print(f"Quantidade de funções: {functionCont}")
    print(f"Quantidade de recursões (máximo de chamadas em uma linha): {recursoesNaLinha}")
    print(f"Complexidade no pior caso: {piorCaso}")
    print(f"Complexidade no melhor caso: {melhorCaso}")

    print("\nCusto computacional:")
    print(f"Custo 1 (operações e comparações): {oper}")
    print(f"Custo N (loops): {repet}")
    print(f"Custo total estimado: {custo_total}")

    print("\nAnálise Assintótica:")
    print(f"Big O: {piorCaso}")
    print(f"Big Omega: {melhorCaso}")
    print(f"Big Theta: {bigTheta}")


def main():
    diretorio = "algoritmo.py"
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
