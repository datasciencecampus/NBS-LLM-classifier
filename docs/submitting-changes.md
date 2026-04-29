## Submitting changes to the NBS-LLM-classifier repo

The following is a suggested git workflow for contributing features and bug fixes to the main NBS-LLM-classifier repo.

## Create a Fork
Visit the [NBS-LLM-classifier](https://github.com/datasciencecampus/NBS-LLM-classifier) repo and click the 'Fork' button. Then use the command line to clone your fork to your local machine.

```bash
git clone https://github.com/USERNAME/NBS-LLM-classifier.git
```

See also: [Forking a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

## Tracking the original repo
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

## Create a Branch
It is important to create a branch on your fork to keep your work separate from the live codebase on `main`. This will ensure that there are no conflicts when you merge the upstream repo's `main` branch into your fork. 

To create and check out a new branch run:

```bash
git switch -c <newbranch>
```

Then commit and push your changes to GitHub. 

See also: [Creating and deleting branches within your repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)

## Submit a Pull Request
Visit your fork of NBS-LLM-classifier on GitHub, select your <newbranch>, and click the pull request button.

See also: [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)