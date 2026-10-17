# Changelog

Todas as mudanças importantes deste projeto ficam registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [0.1.1] — 2026-10-17

### Corrigido
- **A captura não funcionava em sessões reais.** O gatilho passava o texto do
  prompt como argumento de linha de comando; numa transcrição real isso estoura
  o limite do sistema (~128 KB) e falhava **em silêncio**, sem guardar nada.
  Agora o prompt vai pela entrada padrão (stdin).
- **O índice `MEMORY.md` saía vazio.** A checagem de arquivo gerenciado lia só os
  primeiros 400 caracteres; cabeçalhos longos escondiam o marcador `managed_by`,
  e o índice não listava os fatos. Agora lê o arquivo inteiro.

### Melhorado
- Regras de destilação mais rígidas: nada de "meta-memórias" (veredictos sobre
  testes/avaliações), **um único idioma por memória**, e identificadores (nomes,
  caminhos, códigos) copiados exatamente como aparecem.

[0.1.1]: https://github.com/forjadeskills/super-memory/releases/tag/v0.1.1

## [0.1.0] — 2026-10-16

Primeiro lançamento público. 🎉

### Adicionado
- Memória automática de baixo ruído: ao fim de cada sessão, um gatilho `Stop`
  destila só os fatos duráveis — um fato limpo por arquivo.
- Captura 100% local; segredos são apagados antes de salvar.
- Atualização em vez de duplicação (um fato novo que contradiz um antigo o
  substitui).
- Segurança: só mexe em arquivos marcados `managed_by: super-memory`; no
  `MEMORY.md` só reescreve o próprio trecho entre marcadores.
- Instalação como plugin do Claude Code (`/plugin`) ou pelo `install.sh`.
- Comando `/memory-review` para revisar e limpar os fatos guardados.
- Skill `super-memory` para uso manual (lembrar, escrever, podar).
- Demonstração animada (GIF + MP4) no README.

[0.1.0]: https://github.com/forjadeskills/super-memory/releases/tag/v0.1.0
