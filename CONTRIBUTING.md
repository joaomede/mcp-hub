# Commitizen + Conventional Commits + Changelog

## Fluxo recomendado

1. Instale as dependências (Node.js >= 16):
   ```bash
   npm install --save-dev commitizen cz-conventional-changelog @commitlint/cli @commitlint/config-conventional husky standard-version
   npx husky install
   ```
2. Faça commits usando:
   ```bash
   npm run commit
   ```
   (ou `npx cz`)

3. Antes de push, os commits serão validados pelo commitlint.

4. Gere changelog e nova versão:
   ```bash
   npm run release
   # ou apenas npm run changelog
   ```
   Isso atualiza o CHANGELOG.md e o versionamento no package.json.

## Arquivos criados
- `package.json` (scripts e dependências)
- `commitlint.config.js` (validação de commit)
- Husky será inicializado automaticamente no prepare

## Dicas
- Use sempre `npm run commit` para garantir o padrão.
- O changelog é gerado automaticamente a partir dos commits convencionais.
- Para CI/CD, pode-se integrar o semantic-release.
