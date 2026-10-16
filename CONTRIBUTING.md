# Contribuindo com a Super-Memory 💜

Que bom te ver aqui! Este projeto faz parte da **Forja de Skills**, e a nossa
missão é simples: boas ferramentas de IA para quem está **começando**. Então,
se você é iniciante, **este é um ótimo lugar pra fazer sua primeira contribuição
open source** — a gente ajuda no caminho.

## Jeitos de ajudar (do mais simples ao mais técnico)

- ⭐ **Dê uma estrela** no repositório — ajuda MUITO na visibilidade.
- 🐛 **Achou um bug?** Abra uma issue contando o que aconteceu.
- 💡 **Tem uma ideia?** Abra uma issue de ideia, mesmo que pareça pequena.
- 📖 **Melhorar a documentação** (corrigir um texto, traduzir, dar exemplos) é
  uma contribuição valiosíssima e perfeita pra começar.
- 🧪 **Testar e dar feedback** sobre o que a memória guardou (ruído? faltou
  algo?) — é o coração do projeto.
- 🔧 **Código:** melhorias nas regras de destilação (`lib/distill-prompt.md`) ou
  no aplicador (`lib/apply.py`).

## Como mandar uma mudança (passo a passo pra iniciante)

1. Clique em **Fork** (cria uma cópia sua do projeto).
2. Baixe sua cópia: `git clone https://github.com/SEU_USUARIO/super-memory.git`
3. Crie um branch: `git checkout -b minha-melhoria`
4. Faça a mudança e teste.
5. `git commit -m "descreva sua mudança"` e `git push`
6. No GitHub, clique em **Compare & pull request**. Pronto! 🎉

Não precisa ter tudo perfeito — a gente revisa junto, sem julgamento.

## Rodando o projeto localmente

É de propósito **simples**: um gatilho em bash + um aplicador em Python puro
(sem dependências). Dá pra ler tudo numa sentada.

- O gatilho: `hooks/super-memory-capture.sh`
- As regras do que vira memória: `lib/distill-prompt.md`
- O aplicador (cria/atualiza/apaga com segurança): `lib/apply.py`
- Teste rápido do aplicador:
  ```bash
  echo '{"memories":[{"action":"upsert","name":"teste","title":"Teste","hook":"só um teste","description":"x","type":"project","body":"Funciona!"}]}' \
    | python3 lib/apply.py /tmp/sm-teste
  ```

## Combinado de convivência

Seja gentil. Todo mundo aqui está aprendendo. Perguntas "básicas" são bem-vindas
e respondidas com respeito. Zero tolerância a grosseria.

Obrigado por forjar junto. ⚒️
