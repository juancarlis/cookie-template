# Conventional Commits Guide

## Introduction
---

Conventional Commits is a lightweight specification for commit messages that follows a set of simple rules to facilitate the creation of an explicit commit history. This is especially useful for automatically generating changelogs and determining semantic versions.

### Structure of a Commit Message

A commit message should be structured as follows:

```
<type>[optional: scope]: <description>

[optional body]

[optional footer]
```

### Commit Types
- `feat`: a new feature is introduced with the changes.
- `fix`: a bug fix has occurred.
- `chore`: changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies).
- `refactor`: refactored code that neither fixes a bug nor adds a feature.
- `docs`: updates to documentation such as a the README or other markdown files.
- `style`: changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
- `test`: including new or correcting previous tests.
- `perf`: performance improvements.
- `ci`: continuous integration related.
- `build`: changes that affect the build system or external dependencies.
- `revert`: reverts a previous commit.

- `BREAKING CHANGE`: Introduces a change that breaks the API (corresponds with MAJOR in semantic versioning).

### Examples of Commit Messages

1. Commit with description and breaking change footer:

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```
2. Commit with ! to draw attention to breaking change:

```
feat!: send an email to the customer when a product is shipped
```

3. Commit with no body:

```
docs: correct spelling of CHANGELOG
```

4. Commit with scope:

```
feat(lang): add Polish language
```

### Additional Best Practices

- Capitalization and Punctuation: Capitalize the first word and do not end in punctuation.
- Imperative Mood: Use imperative mood in the subject line. Example: "Add fix for dark mode toggle state."
- Length: The first line should ideally be no longer than 50 characters, and the body should be restricted to 72 characters.
- Content: Be direct, try to eliminate filler words and phrases.

## Why Use Conventional Commits?
---

- Automatic changelog generation.
- Automatic semantic version bump.
- Facilitates contributions to your projects by allowing for a more structured commit history.

--- 

This guide is based on the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification) and [tips for writing better commit messages](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/).

