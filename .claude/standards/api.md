# The handler/response contract, modularized out of CLAUDE.md so it stays focused.
- Every public function either raises a domain error or returns a structured result
  ({"ok": true, ...} / {"ok": false, "error": ...}) — never a silent empty dict.
- Document each failure case in the docstring: what it raises, what it returns on a miss.