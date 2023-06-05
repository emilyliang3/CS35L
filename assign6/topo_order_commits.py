import os
import sys
import zlib


class CommitNode:
    """
    Representation of git commit object.

    Attributes:
        commit_hash (str): commit's SHA ID
        parents (list): commit parents
        children (list): commit children
    """

    def __init__(self, commit_hash, parents, children):
        self.commit_hash = commit_hash
        self.parents = parents[:]
        self.children = children[:]

    def get_children(self):
        return self.children

    def add_child(self, child_hash):
        if child_hash not in self.children:
            self.children.append(child_hash)

    def remove_child(self, child_hash):
        self.children.remove(child_hash)

    def get_parents(self):
        return self.parents

    def remove_parent(self, parent_hash):
        self.parents.remove(parent_hash)

    def copy(self):
        return CommitNode(self.commit_hash, self.parents[:], self.children[:])

    def __str__(self):
        return f"Commit Hash: {self.commit_hash}\n\
        Parents: {self.parents}\nChildren: {self.children}"


def get_commits(branches):
    """
    Builds commit graph for all reachable commits.

    Attributes:
        branches (dict): dictionary mapping all
        commits pointed to by branch heads to
        branch names

    Returns:
        dict(str:CommitNode): dict of all commit IDs to their
        CommitNode objects
        list(str): all root commits (lead nodes)
    """
    commits = {}
    root_commits = []
    branch_heads = list(branches.keys())
    # Sort branches for deterministic output:
    sorted_branches = sorted(branch_heads)
    # Perform a dfs starting at each branch head.
    for branch in sorted_branches:
        dfs(branch, commits, root_commits)
    return commits, root_commits


def dfs(commit, commits, roots):
    """
    Perform depth first search on a commit.

    Attributes:
        commit (str): starting commit
        commits (dict(str:CommitNode)): all commit
        objects in the commit graph
        roots (list(str)): all root commits

    Returns:
        none
    """
    cur_commit = commit
    cur_child = []
    remaining_commits = []
    # Continue until every commit is found and nothing left to search.
    while (cur_commit not in commits or remaining_commits):
        cur_parents = get_commit_parents(cur_commit)
        # If current commit already exists add previous commit
        # to its children and set current commit to an unvisited one
        if cur_commit in commits:
            commits[cur_commit].add_child(cur_child[0])
            cur_commit, cur_child = remaining_commits.pop(0)
        # If unvisited commit already exists add current child to
        # its children.
        if cur_commit in commits:
            commits[cur_commit].add_child(cur_child)
        # Else create new CommitNode and add to existing commits.
        else:
            commits[cur_commit] = CommitNode(
                cur_commit, cur_parents, cur_child)
        cur_child = [cur_commit]
        # If current commit has no parents it's a root commit.
        if not cur_parents:
            roots.append(cur_commit)
            # If no more unvisited commits, done searching.
            if not remaining_commits:
                break
            cur_commit, cur_child = remaining_commits.pop(0)
        else:
            unsearched_parents = []
            for parent in cur_parents:
                # If parent already exist, add current commit as
                # a child to it
                if parent in commits:
                    commits[parent].add_child(cur_commit)
                # Otherwise add parent to unvisited commits
                else:
                    unsearched_parents.append((parent, [cur_commit]))
            # Set current commit to first unvisited parent.
            if unsearched_parents:
                cur_commit, cur_child = unsearched_parents.pop(0)
                remaining_commits.extend(unsearched_parents)
            # If no unvisited parents visit next unvisited commit.
            elif remaining_commits:
                cur_commit, cur_child = remaining_commits.pop(0)
            # If no more unvisited commits, done searching.
            else:
                break


def get_commit_parents(commit):
    """
    Get parents of commit (str).
    """
    parents = []
    commit_file = get_object_contents(commit).split('\n')
    for line in commit_file:
        if line.startswith("parent"):
            parents.append(line.split()[1])
    return parents


def get_object_contents(obj):
    """
    Get contents of a git object file.

    Attributes:
        obj (str): target object

    Returns:
        str: zlib decompressed and utf-8 decoded contents
    """
    obj_path = os.path.join(get_git_dir(), 'objects', obj[:2], obj[2:])
    with open(obj_path, "rb") as obj_file:
        return zlib.decompress(obj_file.read()).decode("utf-8")


def get_branch_heads(heads_path):
    """
    Get dictionary of branch heads.

    Attributes:
        heads_path (str): full file path for .git/refs/heads

    Returns:
        dict(str: list(str)): dictionary of commit IDs to
        branch names pointing to that commit ID
    """
    branch_heads = {}
    branches = get_local_branches(heads_path)
    for branch_name in branches:
        branch_path = os.path.join(heads_path, branch_name)
        if os.path.exists(branch_path):
            with open(branch_path, 'r') as branch_ref:
                # Get commit hash from contents of file
                commit_hash = (branch_ref.read().rstrip("\n"))
                # Check if another branch points to same commit hash:
                if commit_hash in branch_heads:
                    branch_heads[commit_hash].append(branch_name)
                else:
                    branch_heads[commit_hash] = [branch_name]
    return branch_heads


def get_git_dir():
    """
    Returns full path of .git file in first git repository
    found, if any.
    """
    cur_dir = os.getcwd()
    # Continue searching until reach root directory:
    while cur_dir != '/':
        # If .git is found, return its path:
        if os.path.isdir(os.path.join(cur_dir, '.git')):
            return os.path.join(cur_dir, '.git')
        # Else search parent directory.
        cur_dir = os.path.dirname(cur_dir)
    # .git directory not found.
    sys.stderr.write('Not inside a Git repository\n')
    exit(1)


def get_local_branches(heads_path):
    """
    Get list of all local branches.

    Attributes:
        heads_path (str): full file path for .git/refs/heads

    Returns:
        list(str): list of branch names
    """
    branches = []
    if os.path.exists(heads_path):
        # Get list of contents of heads directory
        heads_files = os.listdir(heads_path)
        for branch_name in heads_files:
            full_name = branch_name
            # For branch names with slashes, treat each part separated by
            # slashes as a directory.
            while not os.path.isfile(os.path.join(heads_path, full_name)):
                # Follow path to end and concatenate contents.
                full_name += '/' + os.listdir(
                    os.path.join(heads_path, full_name))[0]
            branches.append(full_name)
    return branches


def topo_order(original_commits, original_roots):
    """
    Generate a (reverse) topological ordering of all commits.
    Uses Kahn's algorithm.

    Attributes:
        original_commits (dict(str:CommitNode)): all commits
        original_roots (list(str)): root commits

    Returns:
        list(str): commit IDs topologically sorted
    """
    # Create deep copies because need to preserve original
    # version of attributes.
    commits = {k: v.copy() for k, v in original_commits.items()}
    roots = original_roots[:]
    sorted_commits = []
    while roots:
        # Remove a node from roots and add to sorted list.
        cur_commit = roots.pop(0)
        sorted_commits.append(cur_commit)
        # For each child of the removed node:
        children = commits[cur_commit].get_children().copy()
        for child in children:
            # Remove edge between removed node and child
            commits[cur_commit].remove_child(child)
            commits[child].remove_parent(cur_commit)
            # If child has no other parents, add child
            # to sorted list
            if not commits[child].get_parents():
                roots.append(child)
    return sorted_commits


def print_topo(sorted_commits, commits, branches):
    """
    Print topologically sorted commit hashes from least to greatest.

    Attributes:
        sorted_commits (list(str)): sorted commit hashes
        commits (dict(str:CommitNode)): all commits
        branches (dict(str:list(str))): all branches

    Returns:
        none
    """
    prev_commit_parents = []
    first_iteration = True
    # Print in reverse order because topo_order() returns
    # greatest to least.
    for commit in sorted_commits[::-1]:
        # Check for and print sticky end.
        if not first_iteration and commit not in prev_commit_parents:
            print(" ".join(
                str(parent) for parent in prev_commit_parents) + "=\n")
            print("=" + " ".join(
                str(child) for child in commits[commit].get_children()))
        # Can't have sticky before on first commit.
        if first_iteration:
            first_iteration = False
        # Check if commit is pointed to by a branch.
        if commit in branches:
            sorted_branch_names = sorted(branches[commit])
            # Print alphanumerically sorted branch names.
            print(
                str(commit) + " " + " ".join(
                    str(branch_name) for branch_name in sorted_branch_names
                )
            )
        else:
            print(commit)
        prev_commit_parents = commits[commit].get_parents()


def topo_order_commits():
    """
    Driver function for printing topologically ordered commits.

    Doesn't use other commands. Verified by running
    strace -f -o topo-test.tr pytest followed by
    grep -v "^2863040" topo-test.tr which outputted nothing.
    (2863040 was the PID running the program)
    """
    branches = get_branch_heads(os.path.join(get_git_dir(), 'refs', 'heads'))
    commits, roots = get_commits(branches)
    print_topo(topo_order(commits, roots), commits, branches)


if __name__ == '__main__':
    topo_order_commits()
