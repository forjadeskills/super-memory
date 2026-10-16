# Changelog

Todas as mudanças importantes deste projeto ficam registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

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
