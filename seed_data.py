"""
Dados de seed para a Batalha Olímpica - Semana Olímpica da UFBA 2026.
Importado por database.py durante init_db().

Cada questão é uma tupla (enunciado, imagem_filename_ou_None).
"""

ADMIN_PASSWORD = "gxGWffDOuX"

JUIZES = [
    ("yan.machado",       "xo9cZNlMEk"),
    ("nicholas.cook",     "5udIg@i4LA"),
    ("jose.suzart",       "sJWg5YnWR!"),
    ("juliana.maria",     "bw0cfvnUVU"),
    ("ester.sousa",       "v4V@lzzcGG"),
    ("nicolle.vitoria",   "YV8YYFMsRY"),
    ("felipe.brasileiro", "i4HR54D3pf"),
    ("pablo.vidal",       "0fp@v0dLYO"),
]

# Estrutura: REGATAS[dia]["questoes"][regata_num] = [(enunciado, imagem), ...]
# Dia 1 = facil, Dia 2 = medio, Dia 3 = dificil
REGATAS = {
    1: {
        "nivel": "facil",
        "questoes": {
            1: [
                ("Na figura, o número 7 ocupa a casa central. É possível colocar os números 1, 2, 3, 4, 5, 6, 8 e 9, um em cada uma das casas restantes, de modo que a soma dos números na horizontal seja igual à soma dos números na vertical. Qual é essa soma?",
                 "d1_r1_q1_cruz7.png"),
                ("No refeitório de uma escola de Salvador, na hora do almoço, 130 alunos comeram carne e 150 comeram macarrão, sendo que 1/6 dos alunos comeram também macarrão. Além disso, 70 alunos não comeram carne nem macarrão. Quantos alunos comeram carne, mas não comeram macarrão?",
                 None),
                ("Os números naturais x e y são tais que x·y + x + y = 2024. Qual o valor de x + y?",
                 None),
            ],
            2: [
                ("Há 4 potes de doces. O primeiro pote tem o dobro de doces que o segundo. O terceiro pote tem o triplo de doces que o segundo, e o quarto pote tem 10 doces. Se os quatro potes contêm um total de 70 doces, quantos doces há no primeiro pote?",
                 None),
                ("Joãozinho coleciona números naturais cujo algarismo das unidades é a soma dos outros algarismos. Por exemplo, ele colecionou 10023, pois 1+0+0+2=3. Qual é o maior número sem o algarismo 0 que pode aparecer na coleção?",
                 "d1_r2_q2_joaozinho.png"),
                ("Na figura abaixo, o ponto O no interior do retângulo ABCD é tal que OF = 2, OG = 6, OH = 3 e OI = 1. Os segmentos FG e HI são paralelos aos lados AB e BC, respectivamente. Calcule OB² + OD².",
                 "d1_r2_q3_retangulo_o.png"),
            ],
            3: [
                ("Sejam A = {1, 2, 3, ..., 20} e B = {1, 2, 3, ..., 30} e C = {x ∈ ℤ | x = a - b, a ∈ A e b ∈ B}. Dessa forma, determine o número de elementos do conjunto C.",
                 None),
                ("Carlinhos completou 5 voltas e meia correndo ao longo de uma pista circular. Em seguida, inverteu o sentido e correu mais quatro voltas e um terço, faltando percorrer 40 metros para chegar ao ponto de início. Quantos metros tem essa pista de corrida?",
                 None),
                ("Uma função f é tal que f(x·y) = f(x) + f(y) para quaisquer números reais x e y diferentes de zero. Se f(6) = 4, qual é o valor de f(5)?",
                 None),
            ],
            4: [
                ("Cinco dados foram lançados e a soma dos pontos obtidos nas faces de cima foi 19. Em cada um desses dados, a soma dos pontos da face de cima com os pontos da face debaixo é sempre 7. Qual foi a soma dos pontos obtidos nas faces debaixo?",
                 None),
                ("Morgana escolheu seis números inteiros positivos e diferentes entre si, cuja soma é 2020. Qual é o maior número que pode aparecer dentre os números escolhidos?",
                 None),
                ("Um jogo de Tangram foi construído com sete peças recortadas de um quadriculado no qual o lado de cada quadradinho mede 1 cm, conforme a figura abaixo. A figura a seguir foi montada com 4 dessas peças sem sobreposição. Qual é a área dessa figura?",
                 "d1_r4_q3_tangram.png"),
            ],
            5: [
                ("A figura mostra um quadrado de centro O e área 20 cm². O ponto M é o ponto médio de um dos lados. Qual é a área da região sombreada?",
                 "d1_r5_q1_quadrado_om.png"),
                ("Duas linhas de números são dadas. O número resultante em cada linha deve ser calculado separadamente com base nas regras a seguir, e a pergunta abaixo das linhas de números deve ser respondida. As operações entre os números são realizadas da esquerda para a direita.\nRegras:\n(i) Se um número par é seguido por outro número par, eles devem ser somados.\n(ii) Se um número par é seguido por um número primo, eles devem ser multiplicados.\n(iii) Se um número ímpar é seguido por um número par, o número par deve ser subtraído do número ímpar.\n(iv) Se um número ímpar é seguido por outro número ímpar, o primeiro número deve ser somado ao quadrado do segundo.\n(v) Se um número par é seguido por um número ímpar composto, o número par deve ser dividido pelo número ímpar.\n1ª linha: 36  13  39\n2ª linha: 77  30  7\nQual será o resultado se o valor obtido da segunda linha for dividido pelo valor obtido da primeira linha?",
                 None),
                ("De quantas maneiras podemos trocar uma nota de R$ 20,00 por moedas de R$ 0,10 e R$ 0,25?",
                 None),
            ],
        },
    },
    2: {
        "nivel": "medio",
        "questoes": {
            1: [
                ("Uma moto percorre 1 km por minuto. Em quantos porcento deve ser aumentada a sua velocidade para ela percorrer 1 km em 40 segundos?",
                 None),
                ("Qual a soma dos algarismos do número 10²⁰²⁴ - 2024?",
                 None),
                ("A soma de dois números é 3 e a soma dos seus cubos é 25. Qual é a soma de seus quadrados?",
                 None),
            ],
            2: [
                ("Cada livro da biblioteca municipal de Quixajuba recebe um código formado por três das 26 letras do alfabeto. Eles são colocados em estantes em ordem alfabética: AAA, AAB, ..., AAZ, ABA, ABB, ..., ABZ, ..., AZA, AZB, ..., AZZ, BAA, BAB e assim por diante. O código do último livro é DAB. Quantos livros há na biblioteca?",
                 "d2_r2_q1_livros.png"),
                ("Três medidas positivas são lados de um triângulo se qualquer uma delas é menor que a soma das outras duas. Na figura ao lado, os triângulos ABC e ABD possuem os três lados de comprimentos inteiros. Sabendo que AC = 3, BC = 4, AD = 8 e BD = 10, determine a quantidade de valores inteiros possíveis para a medida do lado AB.",
                 "d2_r2_q2_triangulos.png"),
                ("Sabendo que a + b + c = 1, a² + b² + c² = 2 e a³ + b³ + c³ = 3, qual é o valor de a⁴ + b⁴ + c⁴?",
                 None),
            ],
            3: [
                ("Fernanda precisa criar uma senha para poder usar o computador da escola. A senha deve ter cinco algarismos distintos de modo que, da esquerda para a direita, o algarismo da 1ª posição seja maior do que 1, o da 2ª posição seja maior do que 2, e assim por diante. Por exemplo, 25476 é uma senha possível, mas 52476 não é, pois o algarismo na segunda posição não é maior do que 2. Se a senha de Fernanda começar com 9467, qual deve ser o algarismo da 5ª posição?",
                 None),
                ("Para fazer 24 pães, um padeiro usa exatamente 1 quilo de farinha de trigo, 6 ovos e 200 gramas de manteiga. Qual é o maior número de pães que ele conseguirá fazer com 12 quilos de farinha, 54 ovos e 3,6 quilos de manteiga?",
                 None),
                ("Seja f uma função tal que f(x + y) = f(x)·f(y) para quaisquer x, y ∈ ℝ. Se f(1) = 3, determine o valor de f(1)/f(2) + f(2)/f(3) + ... + f(9)/f(10).",
                 None),
            ],
            4: [
                ("É recomendável que o peso total da mochila com o material escolar de um estudante não ultrapasse 12% do peso do estudante. Ana pesa 48 quilogramas e sua mochila vazia pesa 760 gramas. Qual é o peso máximo recomendado para o material escolar que Ana pode levar em sua mochila?",
                 None),
                ("A mãe de Lúcia pediu para ela não comer mais de 10 docinhos por dia. Além disso, se em um dia ela comer mais de 7 docinhos, nos dois dias seguintes não poderá comer mais de 5 docinhos em cada dia. Qual é o maior número de docinhos que Lúcia pode comer durante um período de 29 dias seguidos, obedecendo ao pedido de sua mãe?",
                 None),
                ("Uma função f é tal que, para cada inteiro positivo n, f(n) = f(n-1) + a·f(n-2), sendo a um número real, f(1) = 1 e f(2) = 2. Sabendo disso, determine o valor de f(5).",
                 None),
            ],
            5: [
                ("Um grupo de 14 amigos comprou 8 pizzas. Eles comeram todas as pizzas, sem sobrar nada. Se cada menino comeu uma pizza inteira e cada menina comeu meia pizza, quantas meninas havia no grupo?",
                 None),
                ("Considere o triângulo ABC a seguir tal que AB = 3, AC = 4 e BC = 5. Sobre o lado BC, são marcados os pontos D e E de modo que BD = 1, DE = 2 e EC = 2. Determine a medida do ângulo ∠DAE.",
                 "d2_r5_q2_triangulo_dae.png"),
                ("Um número natural n, escrito na base 10, tem seis dígitos, sendo 2 o primeiro. Se movermos o dígito 2 da extrema esquerda para a extrema direita, sem alterar a ordem dos dígitos intermediários, o número resultante é três vezes o número original. Determine n.",
                 None),
            ],
        },
    },
    3: {
        "nivel": "dificil",
        "questoes": {
            1: [
                ("Um cubo grande é mergulhado em um recipiente cheio de tinta. Ao retirar o cubo, observa-se que todas as suas faces estão pintadas. Este cubo grande é então cortado em 729 cubos pequenos, porém idênticos. Quantos desses cubos menores têm exatamente duas faces pintadas?",
                 None),
                ("Encontre a soma de todos os inteiros positivos que dão quociente igual ao quadrado do resto quando divididos por 15.",
                 None),
                ("Na figura abaixo, ABCD é um retângulo e os segmentos AQ, BP, CN e DM são tangentes ao círculo de centro O. Se CN=10, BP=8 e DM=7, determine o comprimento de AQ.",
                 "d3_r1_q3_retangulo_circ.png"),
            ],
            2: [
                ("Rosana anotou quantas frutas de cada tipo ela tem, mas alguns números foram borrados. Ela tem 106 frutas no total. Ela tem a mesma quantidade de dois tipos de frutas, e tem o dobro de um tipo de fruta em comparação a outro. Ela tem mais de 10 frutas de cada tipo. Quantas bananas Rosana tem?",
                 "d3_r2_q1_frutas.png"),
                ("Ana e Beto foram os únicos candidatos na eleição para a presidência do grêmio estudantil da escola em que ambos estudam. Nessa eleição, votaram ao todo 1450 alunos. Durante a apuração, houve um momento em que Ana teve a certeza de que, ao final, ela teria pelo menos a metade dos votos válidos. Naquele momento, os percentuais eram os seguintes: votos não válidos: 20% dos votos apurados; votos em Ana: 60% dos votos válidos; votos em Beto: 40% dos votos válidos. Quantos votos tinham sido apurados até aquele momento?",
                 None),
                ("Se x² + y² = 1, então determine o valor de (1 + x + y·i)¹⁰ + (1 + x - y·i)¹⁰, onde i = √(-1).",
                 None),
            ],
            3: [
                ("Luciano queria calcular a média aritmética dos números naturais de 1 a 15. Ao calcular a soma desses números, ele esqueceu de somar dois números consecutivos. Após dividir a soma dos treze números por 15, obteve 7 como resultado. Qual é o produto dos números que Luciano esqueceu de somar?",
                 None),
                ("Um inteiro positivo de 2 dígitos é dito ser interessante se ele é igual à soma de seu dígito das dezenas não nulo e o quadrado de seu dígito das unidades. Quantos inteiros positivos de 2 dígitos são interessantes?",
                 None),
                ("Considere os triângulos △ABC em que BC = 32 e AB/AC = 3. Determine o maior valor possível para a altura relativa ao lado BC.",
                 None),
            ],
            4: [
                ("Na figura, OA = OB = OC. Os pontos A, O e D estão alinhados, e os pontos D e E no segmento BC são tais que BD = DE = EC = OD = OE. Determine o ângulo BÔE.",
                 "d3_r4_q1_angulo_boe.png"),
                ("Dada a sequência de equações x₁ + 1/x₂ = 1, x₂ + 1/x₃ = 1, ..., calcule o valor de x₁ + x₂ + x₃ + ... + x₂₀₂₄.",
                 None),
                ("Escolhem-se aleatoriamente três números distintos no conjunto {1, 2, 3, ..., 100}. Determine a probabilidade de a soma desses três números ser divisível por 3.",
                 None),
            ],
            5: [
                ("Adão atribuiu um valor numérico a cada letra do alfabeto. Multiplicando os valores atribuídos às letras, ele obteve PAPAI=12, GALO=5 e PAPAGAIO=24. Qual é o valor que ele atribuiu à letra L?",
                 None),
                ("Se f é uma função tal que f(x) + 2·f(1-x) = x² para todo x ∈ ℝ, qual é o valor de f(4)?",
                 None),
                ("Um atirador dispõe de três alvos para acertar. O primeiro deste encontra-se a 30m de distância; o segundo, a 40m; o terceiro alvo, a 60m. Sabendo que a probabilidade de o atirador acertar o alvo é inversamente proporcional ao quadrado da distância e que a probabilidade de ele acertar o primeiro alvo é de 2/3, qual a probabilidade de acertar ao menos um dos alvos?",
                 None),
            ],
        },
    },
}
