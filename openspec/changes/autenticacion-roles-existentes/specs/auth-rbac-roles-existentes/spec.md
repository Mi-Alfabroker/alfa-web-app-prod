## ADDED Requirements

### Requirement: User authentication for administrative API access
The system SHALL require valid user authentication before granting access to protected administrative endpoints.

#### Scenario: Successful login issues session tokens
- **WHEN** a user submits valid credentials (usuario and clave) through the authentication endpoint
- **THEN** the system returns a successful response with session tokens and authenticated user context, including tipo_usuario

#### Scenario: Invalid credentials are rejected
- **WHEN** a user submits invalid credentials
- **THEN** the system returns an authentication error and does not issue session tokens

#### Scenario: Missing or invalid access token blocks protected requests
- **WHEN** a client calls a protected endpoint without a valid access token
- **THEN** the system returns HTTP 401 Unauthorized

### Requirement: Role-based authorization with existing domain roles
The system SHALL enforce authorization rules using existing roles AGENTE, ADMINISTRADOR, SUPERADMIN, and CLIENTE for all protected backend operations.

#### Scenario: Authorized role can access protected action
- **WHEN** a user with a role allowed by the endpoint policy invokes that endpoint
- **THEN** the system allows the operation and returns a success response

#### Scenario: Authenticated but unauthorized role is denied
- **WHEN** an authenticated user invokes an endpoint not allowed for their role
- **THEN** the system returns HTTP 403 Forbidden

#### Scenario: Administrative roles are accepted for admin-protected operations
- **WHEN** a user with role ADMINISTRADOR or SUPERADMIN invokes an admin-protected endpoint
- **THEN** the system authorizes the request according to admin policy

### Requirement: Secure credential handling
The system MUST store user credentials using secure password hashing and MUST NOT persist plaintext passwords.

#### Scenario: New password is stored as hash
- **WHEN** a user account is created or password is updated
- **THEN** the stored credential is a secure hash and not the plaintext value

#### Scenario: Existing plaintext credentials are migrated safely
- **WHEN** the credential migration process runs for existing users
- **THEN** legacy plaintext passwords are replaced with secure hashes without exposing raw credentials in logs or responses

### Requirement: Frontend session and route protection by role
The frontend SHALL manage authenticated session state and restrict route/module access based on authenticated user role.

#### Scenario: Unauthenticated user is redirected to login
- **WHEN** an unauthenticated user navigates to a protected route
- **THEN** the frontend redirects the user to the login flow

#### Scenario: Navigation options are role-aware
- **WHEN** an authenticated user accesses the application shell
- **THEN** the frontend displays only modules/actions permitted for the user role

#### Scenario: Expired session triggers re-authentication flow
- **WHEN** the backend responds that session authentication is no longer valid
- **THEN** the frontend clears session state and redirects to authentication

### Requirement: Standardized auth error contract
The system SHALL provide consistent authentication and authorization error responses for backend and frontend interoperability.

#### Scenario: Unauthorized errors are distinguishable
- **WHEN** a request fails because authentication is missing or invalid
- **THEN** the response is returned with HTTP 401 and a standardized error payload

#### Scenario: Forbidden errors are distinguishable
- **WHEN** a request fails because role authorization is insufficient
- **THEN** the response is returned with HTTP 403 and a standardized error payload
