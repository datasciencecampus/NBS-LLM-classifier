# Contributing to the NBS-LLM-classifier repo

We welcome improvements, bug fixes, or new features to the NBS-LLM-classifier. How to contribute to the repo will depend on whether you have access to the repository.

## Contributors with repository access
Clone the repo and create a branch from `main`.

1. Create a local copy of the remote repository

```bash
git clone https://github.com/datasciencecampus/NBS-LLM-classifier.git
```

2. Create and check out a new branch

```bash
git switch -c <newbranch>
```

3. Make changes, run local checks, stage, and commit

```bash
pre-commit run --all-files
git add .
git commit -m "Commit message"
```

If pre-commit changes any files, review the changes, then stage and commit them.

4. Push the new branch to the remote

```bash
git push -u origin <newbranch>
```

5. Open a pull request in GitHub

See also: [CONTRIBUTING.md](../CONTRIBUTING.md) in the root folder.

## Contributors without repository access
Fork the repository and open a pull request.

1. Create a Fork

Visit the [NBS-LLM-classifier](https://github.com/datasciencecampus/NBS-LLM-classifier) repo and click the 'Fork' button. Then use the command line to clone your fork to your local machine.
```bash
git clone https://github.com/USERNAME/NBS-LLM-classifier.git
```

See also: [Forking a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

2. Track the original repo
To keep your fork up to date you need to track the original upstream repo.

```bash
git remote add upstream https://github.com/datasciencecampus/NBS-LLM-classifier.git
```

When you want to update your fork with the latest upstream changes run:

```bash
git fetch upstream
```

To merge the changes in the upstream repo's `main` branch into your fork's `main` branch run:

```bash
git checkout main
git merge upstream/main
```

See also: [Syncing a fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork)

3. Create a Branch
It is important to create a branch on your fork to keep your work separate from the live codebase on `main`. This will ensure that there are no conflicts when you merge the upstream repo's `main` branch into your fork.

To create and check out a new branch run:

```bash
git switch -c <newbranch>
```

Then make changes, run local checks, commit, and push your branch to GitHub.

```bash
pre-commit run --all-files
git add .
git commit -m "Commit message"
git push -u origin <newbranch>
```

If pre-commit changes any files, review the changes, then stage and commit them.

See also: [Creating and deleting branches within your repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)

4. Open a Pull Request
Visit your fork of NBS-LLM-classifier on GitHub, select your branch, and click the pull request button.

See also: [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
