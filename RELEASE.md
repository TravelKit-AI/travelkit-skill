# Release Process / 发布流程

This repository ships the `travelkit` skill as source files under `skills/travelkit/` and as a zip package at `skills/travelkit.zip`.

本仓库同时发布 `skills/travelkit/` 源文件目录和 `skills/travelkit.zip` 压缩包。

## Release Checklist / 发布检查清单

1. Update `CHANGELOG.md`.
   更新 `CHANGELOG.md`。

2. Rebuild the package.
   重新生成压缩包。

   ```bash
   scripts/package-skill.sh
   ```

3. Run repository checks.
   运行仓库检查。

   ```bash
   scripts/check-skill-package.sh
   git diff --check
   ```

4. Commit the source, changelog, and `skills/travelkit.zip` changes.
   提交源码、changelog 和 `skills/travelkit.zip` 变更。

5. Create and push a version tag.
   创建并推送版本 tag。

   ```bash
   VERSION=v1.0.1
   git tag "$VERSION"
   git push origin "$VERSION"
   ```

6. Create a GitHub Release from the tag and upload `skills/travelkit.zip` as the release artifact.
   基于 tag 创建 GitHub Release，并上传 `skills/travelkit.zip` 作为发布附件。

The existing `v1.0.0` tag is the baseline release. Use the next appropriate version for future releases.

现有 `v1.0.0` tag 是基线版本。后续发布请使用下一个合适版本号。

## Package Rules / 压缩包规则

- `skills/travelkit.zip` must match the current contents of `skills/travelkit/`.
- The package root must be `travelkit/`.
- The package must include `travelkit/SKILL.md` and `travelkit/references/*.md`.
- Do not include local editor files, `.DS_Store`, `__MACOSX`, credentials, logs, real passenger data, or order data.

- `skills/travelkit.zip` 必须与当前 `skills/travelkit/` 内容一致。
- 压缩包根目录必须是 `travelkit/`。
- 压缩包必须包含 `travelkit/SKILL.md` 和 `travelkit/references/*.md`。
- 不要包含本地编辑器文件、`.DS_Store`、`__MACOSX`、凭证、日志、真实乘客信息或订单数据。
