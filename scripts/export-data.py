import json
import os
import sqlite3
import sys
from pathlib import Path


def main():
    home = Path(os.environ.get("USERPROFILE", str(Path.home())))
    db_path = home / ".herdr-mem" / "herdr-mem.db"
    if not db_path.is_file():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "memory-snapshot.json"

    uri = db_path.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        conn.execute("PRAGMA query_only=ON")
        # Fetch newest 1000 active observations across all projects
        rows = conn.execute(
            """
            SELECT o.id, o.session_id, o.occurred_at, o.kind, o.title, o.body, o.fidelity, o.source_key,
                   s.project_id, s.machine_id, s.harness, s.native_session_id
            FROM observations o
            JOIN sessions s ON s.id = o.session_id
            WHERE o.status = 'active'
            ORDER BY o.id DESC
            LIMIT 1000
            """
        ).fetchall()

        # Count total active observations and sessions
        total_obs = conn.execute("SELECT count(*) FROM observations WHERE status='active'").fetchone()[0]
        total_sessions = conn.execute("SELECT count(*) FROM sessions").fetchone()[0]
        projects = [r[0] for r in conn.execute("SELECT DISTINCT project_id FROM sessions ORDER BY project_id").fetchall()]
    finally:
        conn.close()

    items = []
    details = {}
    for r in rows:
        oid = r[0]
        title = r[4] or ""
        body = r[5] or ""
        items.append({
            "id": oid,
            "session_id": r[1],
            "occurred_at": r[2],
            "kind": r[3],
            "title": title,
            "fidelity": r[6],
            "source_key": r[7],
            "project": r[8],
            "machine_id": r[9],
            "harness": r[10],
            "native_session_id": r[11],
            "cost_chars": len(title) + len(body),
        })
        details[str(oid)] = {
            "body": body,
            "source_key": r[7],
            "harness": r[10],
            "session": r[11],
            "fidelity": r[6],
            "project": r[8],
        }

    payload = {
        "version": 1,
        "exported_at": sqlite3.datetime.datetime.now(sqlite3.timezone.utc if hasattr(sqlite3, "timezone") else None).isoformat() if hasattr(sqlite3, "datetime") else "",
        "stats": {
            "total_observations_in_db": total_obs,
            "total_sessions_in_db": total_sessions,
            "exported_observations": len(items),
            "projects": projects,
        },
        "items": items,
        "details": details,
    }

    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Successfully exported {len(items)} observations to {out_file} (Total in DB: {total_obs})")


if __name__ == "__main__":
    main()
