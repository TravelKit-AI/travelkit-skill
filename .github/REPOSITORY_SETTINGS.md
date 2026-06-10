# Repository Settings / 仓库设置

This file documents the GitHub settings maintainers should enable for open source collaboration.

本文件记录维护者应在 GitHub 中开启的开源协作设置。

## Features / 功能

- Enable Issues, Pull Requests, and Discussions.
- Enable Private vulnerability reporting.
- Disable blank issues unless maintainers intentionally want free-form reports.

- 开启 Issues、Pull Requests 和 Discussions。
- 开启 Private vulnerability reporting。
- 关闭空白 Issue，除非维护者明确希望接受自由格式反馈。

## Merge Policy / 合并策略

- Prefer squash merge for pull requests.
- Require pull requests before merging into `main`.
- Require at least one maintainer review before merge.
- Require branches to be up to date before merge when checks are configured.
- Do not allow direct pushes to `main` except for emergency maintainer actions.

- PR 默认建议使用 squash merge。
- 合并到 `main` 前必须经过 Pull Request。
- 合并前至少需要一名维护者审核。
- 配置检查后，要求分支在合并前保持最新。
- 除紧急维护操作外，不允许直接 push 到 `main`。

## Maintainers and Code Owners / 维护者与 Code Owners

- Create a GitHub organization team named `TravelKit-AI/maintainers`.
- Grant that team write access to this repository.
- Keep `.github/CODEOWNERS` in sync with the active maintainer team so pull requests automatically request review.

- 在 GitHub 组织中创建名为 `TravelKit-AI/maintainers` 的团队。
- 授予该团队对本仓库的写权限。
- 保持 `.github/CODEOWNERS` 与实际维护团队一致，这样 PR 才会自动请求 review。

## Project Board / 项目看板

Create a GitHub Project with these columns or statuses:

创建 GitHub Project，并使用以下列或状态：

- `Backlog`
- `Ready`
- `In Progress`
- `Review`
- `Done`

## Issue Triage / Issue 分流

Use labels from `.github/labels.yml` to classify:

使用 `.github/labels.yml` 中的标签分类：

- Type: `bug`, `feature`, `documentation`, `security`, `question`
- Difficulty: `good first issue`, `help wanted`, `needs maintainer input`
- Area: `flight-search`, `booking`, `payment`, `refund`, `change`, `agent-integration`
- Status: `needs reproduction`, `blocked`, `ready for PR`
