# Commitizen + Conventional Commits + Changelog

## Recommended workflow

1. Install dev dependencies (Node.js >= 16):
   ```bash
   npm install --save-dev commitizen cz-conventional-changelog @commitlint/cli @commitlint/config-conventional husky standard-version
   npx husky install
   ```
2. Create commits using:
   ```bash
   npm run commit
   ```
   (or `npx cz`)

3. Commits are validated by commitlint before pushing.

4. Generate changelog and a new release:
   ```bash
   npm run release
   # or just npm run changelog
   ```
   This updates CHANGELOG.md and bumps the version in package.json.

## Generated files
- `package.json` (scripts and dependencies)
- `commitlint.config.js` (commit validation)
- Husky will be initialized automatically on prepare

## Tips
- Always use `npm run commit` to ensure correct commit format.
- The changelog is generated automatically from conventional commits.
- For CI/CD, consider integrating semantic-release.
