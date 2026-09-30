## 2024-05-24 - [Remove hardcoded admin secret]
**Vulnerability:** A hardcoded administrative secret ("admin-secret-123") was used to protect the /api/admin/data and /api/admin/user endpoints in `worker.js`.
**Learning:** Hardcoded credentials in source code pose a critical security risk as they can be extracted by anyone with access to the repository, potentially leading to unauthorized data access and deletion.
**Prevention:** Always use environment variables (e.g., `env.ADMIN_SECRET`) to pass sensitive configuration into Cloudflare Workers and ensure the authentication logic explicitly fails if the environment variable is not set.
