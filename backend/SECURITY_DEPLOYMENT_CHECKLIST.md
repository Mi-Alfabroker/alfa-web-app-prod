# Security Migration and Deployment Checklist

## Backup and Rollback Procedure (Task 4.4)

### Pre-migration backup

1. Create DB backup before password migration:

```bash
pg_dump -h <host> -U <user> -d <database> -F c -f backup_pre_auth_migration.dump
```

2. Verify backup integrity:

```bash
pg_restore -l backup_pre_auth_migration.dump
```

3. Keep backup artifact in secure storage with timestamp and environment label.

### Migration execution

1. Deploy backend with hashing support and auth endpoints.
2. Run idempotent migration script:

```bash
python backend/scripts/migrate_password_hashes.py
```

3. Validate that no `usuarios.clave` values remain in plaintext format.

### Rollback

1. Roll back backend/frontend services to previous image versions.
2. Restore database backup if migration introduced inconsistency:

```bash
pg_restore -h <host> -U <user> -d <database> --clean --if-exists backup_pre_auth_migration.dump
```

3. Verify legacy endpoints and login behavior before opening traffic.

## Staging Validation Plan (Task 6.3)

1. Seed staging with representative users for `SUPERADMIN`, `ADMINISTRADOR`, `AGENTE`, `CLIENTE`.
2. Execute auth flow checks:
   - Login success/failure
   - Refresh token flow
   - `GET /api/auth/me`
3. Execute authorization matrix checks:
   - 200 for allowed roles
   - 403 for forbidden roles
   - 401 for missing/invalid token
4. Run frontend role-navigation checks:
   - Redirect to `/login` when unauthenticated
   - Menu visibility by role
   - Logout flow

## Gradual Deployment Checklist (Task 6.4)

- [ ] Confirm `JWT_SECRET_KEY` and token expiration env vars are set in target environment.
- [ ] Confirm backups generated and verified.
- [ ] Deploy backend auth + RBAC changes.
- [ ] Run password migration script and capture output.
- [ ] Deploy frontend login/session updates.
- [ ] Smoke test key workflows with `ADMINISTRADOR` and `AGENTE` users.
- [ ] Monitor 401/403 rates, login failure rate, and API error logs for 24h.
- [ ] Keep rollback plan and backup identifiers attached to deployment ticket.
