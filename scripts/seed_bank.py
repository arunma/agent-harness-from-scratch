"""Seed a synthetic digital bank in SQLite (plumbing zone).

    uv run python scripts/seed_bank.py            # default size
    uv run python scripts/seed_bank.py --customers 500 --reset

All data is fake and deterministic (fixed random seed). The `merchant_memo`
field is free text on purpose: on Day 3 you will plant prompt-injection
payloads there yourself.
"""

from __future__ import annotations

import random
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import typer

from agent_sprint.config import settings

SCHEMA = """
CREATE TABLE customers (
    customer_id   TEXT PRIMARY KEY,
    full_name     TEXT NOT NULL,
    email         TEXT NOT NULL,
    phone         TEXT NOT NULL,
    segment       TEXT NOT NULL CHECK (segment IN ('retail', 'premier', 'sme')),
    kyc_status    TEXT NOT NULL CHECK (kyc_status IN ('verified', 'pending', 'expired')),
    created_at    TEXT NOT NULL
);
CREATE TABLE accounts (
    account_id    TEXT PRIMARY KEY,
    customer_id   TEXT NOT NULL REFERENCES customers(customer_id),
    product       TEXT NOT NULL CHECK (product IN ('savings', 'current', 'credit_card', 'fixed_deposit')),
    currency      TEXT NOT NULL,
    balance_cents INTEGER NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('active', 'frozen', 'closed')),
    opened_at     TEXT NOT NULL
);
CREATE TABLE transactions (
    txn_id        TEXT PRIMARY KEY,
    account_id    TEXT NOT NULL REFERENCES accounts(account_id),
    posted_at     TEXT NOT NULL,
    amount_cents  INTEGER NOT NULL,          -- negative = debit
    currency      TEXT NOT NULL,
    merchant      TEXT NOT NULL,
    mcc           TEXT NOT NULL,
    channel       TEXT NOT NULL CHECK (channel IN ('card_present', 'online', 'transfer', 'atm')),
    merchant_memo TEXT NOT NULL              -- free text; Day 3 attack surface
);
CREATE TABLE disputes (
    dispute_id    TEXT PRIMARY KEY,
    txn_id        TEXT NOT NULL REFERENCES transactions(txn_id),
    customer_id   TEXT NOT NULL REFERENCES customers(customer_id),
    reason        TEXT NOT NULL CHECK (reason IN ('fraud', 'not_received', 'duplicate', 'wrong_amount', 'cancelled')),
    status        TEXT NOT NULL CHECK (status IN ('open', 'investigating', 'resolved_customer', 'resolved_merchant', 'rejected')),
    opened_at     TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    notes         TEXT NOT NULL DEFAULT ''
);
CREATE TABLE policies (
    policy_id     TEXT PRIMARY KEY,
    title         TEXT NOT NULL,
    body          TEXT NOT NULL,
    access_level  TEXT NOT NULL CHECK (access_level IN ('public', 'internal', 'restricted')),
    effective_on  TEXT NOT NULL
);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_txn_account ON transactions(account_id, posted_at);
CREATE INDEX idx_disputes_customer ON disputes(customer_id);
"""

FIRST = ["Wei Ling", "Arjun", "Siti", "Marcus", "Priya", "Jun Hao", "Aisha", "Daniel", "Mei", "Ravi",
         "Nur", "Ethan", "Kavitha", "Hui Min", "Farhan", "Chloe", "Vikram", "Li Na", "Imran", "Grace"]
LAST = ["Tan", "Lim", "Ng", "Rahman", "Kumar", "Lee", "Wong", "Chua", "Nair", "Goh",
        "Ismail", "Teo", "Pillai", "Koh", "Ong", "Menon", "Yeo", "Hassan", "Chen", "Sim"]
MERCHANTS = [
    ("FairPrice Xtra", "5411", "card_present"), ("Grab Transport", "4121", "online"),
    ("Shopee SG", "5399", "online"), ("Lazada", "5399", "online"), ("SP Group", "4900", "online"),
    ("Kopitiam", "5814", "card_present"), ("Guardian Pharmacy", "5912", "card_present"),
    ("Singtel", "4814", "online"), ("Changi Airport Duty Free", "5309", "card_present"),
    ("Netflix", "4899", "online"), ("Uniqlo ION", "5651", "card_present"),
    ("Golden Village", "7832", "card_present"), ("Foodpanda", "5812", "online"),
    ("PayNow Transfer", "4829", "transfer"), ("ATM Withdrawal", "6011", "atm"),
]
MEMOS = ["", "Thank you for shopping with us", "Order #{n}", "Ref {n}", "Monthly subscription",
         "Split bill", "Refund pending", "Invoice {n}", "Gift", "Groceries"]
SGT = timezone(timedelta(hours=8))

POLICIES = [
    ("POL-001", "Card dispute window", "Customers may raise a card dispute within 60 days of the statement date.", "public"),
    ("POL-002", "Provisional credit", "Provisional credit may be granted for fraud disputes above SGD 100 after verification.", "internal"),
    ("POL-003", "Fraud escalation", "Suspected account takeover must be escalated to the fraud desk within 1 hour.", "restricted"),
    ("POL-004", "Duplicate charges", "Duplicate charges are reversed without investigation when both postings match exactly.", "internal"),
    ("POL-005", "Frozen accounts", "No outgoing transfers may be initiated from a frozen account.", "public"),
]


def main(
    customers: int = typer.Option(200, help="Number of customers."),
    txns_per_account: int = typer.Option(25, help="Average transactions per account."),
    seed: int = typer.Option(42, help="Random seed (deterministic output)."),
    reset: bool = typer.Option(True, help="Delete the existing database first."),
) -> None:
    rng = random.Random(seed)
    path: Path = settings.bank_db_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if reset and path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)

    today = date(2026, 9, 1)
    cust_rows, acct_rows, txn_rows, disp_rows = [], [], [], []
    for c in range(1, customers + 1):
        cid = f"C-{1000 + c}"
        first, last = rng.choice(FIRST), rng.choice(LAST)
        cust_rows.append((
            cid, f"{first} {last}",
            f"{first.lower().replace(' ', '.')}.{last.lower()}{c}@example.com",
            f"+65 9{rng.randint(1000000, 9999999)}",
            rng.choices(["retail", "premier", "sme"], [70, 20, 10])[0],
            rng.choices(["verified", "pending", "expired"], [88, 7, 5])[0],
            (today - timedelta(days=rng.randint(30, 2000))).isoformat(),
        ))
        for a in range(rng.choice([1, 1, 2, 2, 3])):
            aid = f"A-{cid[2:]}-{a + 1}"
            product = rng.choice(["savings", "current", "credit_card", "fixed_deposit"])
            acct_rows.append((
                aid, cid, product, "SGD", rng.randint(-500_000, 5_000_000) if product == "credit_card" else rng.randint(0, 8_000_000),
                rng.choices(["active", "frozen", "closed"], [92, 4, 4])[0],
                (today - timedelta(days=rng.randint(10, 1500))).isoformat(),
            ))
            for t in range(max(1, int(rng.gauss(txns_per_account, 8)))):
                merchant, mcc, channel = rng.choice(MERCHANTS)
                tid = f"T-{aid[2:]}-{t:04d}"
                posted = datetime(2026, 9, 1, tzinfo=SGT) - timedelta(minutes=rng.randint(0, 180 * 24 * 60))
                amount = -rng.randint(150, 45_000) if channel != "transfer" or rng.random() < 0.7 else rng.randint(1_000, 300_000)
                memo = rng.choice(MEMOS).format(n=rng.randint(10000, 99999))
                txn_rows.append((tid, aid, posted.isoformat(timespec="seconds"), amount, "SGD", merchant, mcc, channel, memo))
                if amount < 0 and rng.random() < 0.012:
                    opened = posted + timedelta(days=rng.randint(1, 50))
                    disp_rows.append((
                        f"D-{len(disp_rows) + 1:05d}", tid, cid,
                        rng.choice(["fraud", "not_received", "duplicate", "wrong_amount", "cancelled"]),
                        rng.choice(["open", "investigating", "resolved_customer", "resolved_merchant", "rejected"]),
                        opened.isoformat(timespec="seconds"),
                        (opened + timedelta(days=rng.randint(0, 20))).isoformat(timespec="seconds"), "",
                    ))

    con.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?)", cust_rows)
    con.executemany("INSERT INTO accounts VALUES (?,?,?,?,?,?,?)", acct_rows)
    con.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)", txn_rows)
    con.executemany("INSERT INTO disputes VALUES (?,?,?,?,?,?,?,?)", disp_rows)
    con.executemany("INSERT INTO policies VALUES (?,?,?,?,?)", [(*p, "2026-01-01") for p in POLICIES])
    con.commit()
    con.close()
    typer.echo(f"Seeded {path}: {len(cust_rows)} customers, {len(acct_rows)} accounts, "
               f"{len(txn_rows)} transactions, {len(disp_rows)} disputes, {len(POLICIES)} policies.")


if __name__ == "__main__":
    typer.run(main)
