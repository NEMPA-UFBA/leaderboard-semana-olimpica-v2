# Design: Exclusão de Tentativas

## Problema
Erros no registro de tentativas não podem ser desfeitos. O botão "Corrigir" existente inverte acertou/errou, mas não permite remover tentativas registradas por engano.

## Decisões
- **Localização:** Página do Juiz (2_Juiz.py), no histórico de tentativas existente
- **Permissão:** Juiz pode excluir suas próprias tentativas; admin pode excluir qualquer uma
- **Renumeração:** Ao excluir, tentativas restantes são renumeradas (1, 2, 3) e pontos recalculados
- **Leaderboard:** Atualiza automaticamente (já usa SUM agregado)

## Componentes

### scoring.py — `excluir_tentativa(db, tentativa_id)`
1. Busca tentativa pelo ID
2. Salva equipe_id e questao_id
3. Exclui do banco
4. Busca tentativas restantes (mesma equipe/questão), ordenadas por created_at
5. Renumera sequencialmente e recalcula pontos com PONTOS_POR_TENTATIVA
6. Commit

### pages/2_Juiz.py — Botão "Excluir"
- Aparece ao lado do botão "Corrigir" no histórico
- Visível para: juiz dono da tentativa OU admin
- Ao clicar: chama excluir_tentativa() e faz rerun

## Fluxo
1. Juiz seleciona equipe + questão
2. Vê histórico com botões Corrigir e Excluir
3. Clica Excluir → tentativa removida, restantes renumeradas, pontos recalculados
4. Página atualiza com novo estado
