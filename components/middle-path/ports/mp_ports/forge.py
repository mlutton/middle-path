"""Strict in-memory Forge with an atomic expected-head merge guard."""

from .types import EffectLog, ForgeReason, IssueId, PrId, Sha, Verdict


class ForgeRefused(Exception):
    def __init__(self, reason: ForgeReason) -> None:
        self.reason = reason
        super().__init__(reason)


class MemoryForge:
    def __init__(self, log: EffectLog) -> None:
        self.log = log
        self.issues: dict[IssueId, tuple[str, str]] = {}
        self.prs: dict[PrId, tuple[IssueId, Sha]] = {}
        self.verdicts: list[tuple[PrId, Verdict]] = []
        self.merges: list[tuple[PrId, Sha]] = []

    def create_issue(self, title: str, body: str) -> IssueId:
        self.log.add("forge", "create_issue", title, body)
        issue = len(self.issues) + 1
        self.issues[issue] = (title, body)
        return issue

    def create_pr(self, issue: IssueId, head_sha: Sha) -> PrId:
        self.log.add("forge", "create_pr", issue, head_sha)
        if issue not in self.issues:
            raise ForgeRefused("issue-unknown")
        pr = len(self.prs) + 1
        self.prs[pr] = (issue, head_sha)
        return pr

    def pr_head(self, pr: PrId) -> Sha:
        self.log.add("forge", "pr_head", pr)
        if pr not in self.prs:
            raise ForgeRefused("pr-unknown")
        return self.prs[pr][1]

    def move_head(self, pr: PrId, head: Sha) -> None:
        self.pr_head(pr)
        self.prs[pr] = (self.prs[pr][0], head)

    def post_verdict(self, pr: PrId, verdict: Verdict) -> None:
        self.log.add("forge", "post_verdict", pr, verdict)
        if pr not in self.prs:
            raise ForgeRefused("pr-unknown")
        self.verdicts.append((pr, verdict))

    def merge(self, pr: PrId, expected_head: Sha) -> None:
        self.log.add("forge", "merge", pr, expected_head)
        if pr not in self.prs:
            raise ForgeRefused("pr-unknown")
        if any(merged_pr == pr for merged_pr, _ in self.merges):
            raise ForgeRefused("already-merged")
        if self.prs[pr][1] != expected_head:
            raise ForgeRefused("head-moved")
        self.merges.append((pr, expected_head))
