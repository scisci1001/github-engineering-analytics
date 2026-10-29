# GitHub Engineering Analytics

A Python and MongoDB backend project for collecting and analyzing GitHub repository activity, pull requests, issues, commits, reviews, contributors, and engineering metrics.

---

## 1. Project Purpose

This project is intended as a portfolio-quality backend engineering project that demonstrates:

- Senior-level backend engineering practices
- Python backend development
- MongoDB data modeling and querying
- Integration with an external REST API
- Asynchronous and incremental data ingestion
- API design
- Performance-conscious database access
- Testing and maintainability
- Production-oriented architecture decisions

The project should be suitable for presentation on GitHub and LinkedIn and should provide meaningful discussion topics for technical interviews.

A key design goal is to use MongoDB where its document-oriented model provides a meaningful advantage over a traditional relational design.

---

## 2. Repository Metadata

**Repository name:** `github-engineering-analytics`

**Repository description:**  
`A Python and MongoDB backend for collecting and analyzing GitHub repository activity, pull requests, issues, commits, and engineering metrics.`

---

## 3. Current Project Status

**Current phase:** Project definition and architecture planning

**Overall status:** 🟡 In progress

**Current milestone:** Define the MVP data requirements and MongoDB model before implementation.

**Next step:** Begin implementation planning for the first coding phase.

---

## 4. Project Scope

The application will import data from public GitHub repositories and store relevant information in MongoDB.

The system should eventually support arbitrary public GitHub repositories instead of being hard-coded to one repository.

Initial candidate repositories may include:

- Spring Boot
- FastAPI
- Pydantic
- Other active open-source repositories selected later

The first implementation should deliberately limit imported history so development remains practical and GitHub API rate limits remain manageable.

Possible initial limits:

- 500–2,000 recent commits
- 500 recent pull requests
- 500 recent issues
- Associated reviews
- Contributor information

These numbers are provisional and may be adjusted after testing GitHub API behavior.

---

## 5. High-Level Architecture

Initial target architecture:

```text
GitHub API
    |
    v
Repository Import / Synchronization
    |
    v
MongoDB
    |
    v
Analytics Service
    |
    v
FastAPI REST API
```

Potential future extensions:

```text
Background Jobs / Scheduler
        |
        v
Incremental Synchronization

MongoDB
   |
   +--> Engineering Metrics API
   |
   +--> Search / Analytics
   |
   +--> AI / Semantic Analysis
```

---

## 6. Confirmed Decisions

Decisions in this section are considered accepted unless explicitly changed later.

### D-001 — Project Topic

**Decision:** GitHub repository engineering analytics.

**Reasoning:**  
GitHub provides real-world, heterogeneous, hierarchical JSON data. Repository metadata, pull requests, issues, reviews, commits, users, labels, and related entities differ structurally and provide a credible use case for MongoDB.

The topic also demonstrates external API integration and is directly relevant to software engineering.

---

### D-002 — Primary Technology Focus

**Decision:**

- Python
- MongoDB

The project should demonstrate both technologies as first-class components rather than using either one superficially.

---

### D-003 — Input Data

**Decision:** Use real public GitHub repositories as the primary input source.

Generated data may later be used for testing, performance testing, edge cases, or load simulation, but not as the project's primary dataset.

---

### D-004 — Repository Selection Strategy

**Decision:** The application must eventually support arbitrary public GitHub repositories.

Initial development may use a small number of known repositories for repeatable testing.

The repository selection must therefore be configuration/input driven rather than hard-coded into the domain logic.

---

### D-005 — Portfolio Positioning

**Decision:** The project should look like a senior backend engineering project, not a MongoDB CRUD tutorial.

The implementation should therefore emphasize:

- Architectural separation
- Explicit domain modeling
- API boundaries
- Failure handling
- Idempotency
- Incremental synchronization
- Index design
- Query performance
- Testing
- Maintainability
- Observability
- Documentation of trade-offs

---

### D-006 — MVP Analytics Scope

**Decision:** The MVP will implement exactly seven primary analytics areas:

- Pull request lead time
- Time to first review
- Pull request size statistics
- Pull request size vs. review time
- Contributor activity
- Issue resolution time
- Repository activity trends over time for pull requests and issues

**Reasoning:**  
This set is broad enough to demonstrate meaningful MongoDB aggregation, time-based analysis, relationships between GitHub entities, indexing, and senior backend design without turning the project into a large analytics product.

Repository-level commit activity was intentionally removed from the MVP after the commit-modeling decision in D-007.

Additional metrics are deferred until after the MVP.

---

### D-007 — Commit Modeling

**Decision:** Pull-request commits will be embedded in `pull_requests.commits[]`. The MVP will not use a separate `commits` collection.

**Reasoning:**  
Within the current analytics scope, commits are primarily relevant as part of the pull request aggregate. Embedding them keeps related data together and supports commit-per-PR analytics without unnecessary cross-collection access.

Because direct pushes to the default branch can exist independently of pull requests, repository-wide commit activity would require a separate repository commit model. That metric is not important enough for the MVP to justify the extra collection and synchronization complexity.

**Consequence:** Repository activity trends in the MVP cover pull requests and issues, not repository-wide commit history.

---

### D-008 — MongoDB Document Schema

**Decision:** The MVP uses four top-level collections: `repositories`, `pull_requests`, `issues`, and `sync_states`.

Pull request `reviews[]` and `commits[]` are embedded. Lightweight user identity snapshots are embedded where needed.

Derived analytics values such as lead time, first-review time, commit count, and issue resolution time are calculated in aggregation pipelines rather than persisted.

Indexes are centered on repository-scoped access patterns. Additional multikey indexes will only be introduced when query measurements justify them.

**Reasoning:**  
The schema is designed around the project's analytics use cases and aggregate boundaries rather than mirroring GitHub's API resources or applying relational normalization mechanically.

---

### D-009 — MongoDB Feature Scope

**Decision:** The MVP will use aggregation pipelines as its primary analytics mechanism, together with compound indexes, selective multikey indexes, bulk upserts, schema validation, and `explain()`-based query-plan analysis.

`$unwind` and `$facet` will be used where they naturally support embedded-array analytics and combined repository-level views.

The MVP will defer `$lookup`, change streams, TTL indexes, text search, time-series collections, and window functions unless a concrete requirement emerges.

**Reasoning:**  
The project should demonstrate MongoDB depth through features that solve real problems rather than maximize the number of technologies or operators used.

---


### D-010 — FastAPI Framework

**Decision:** Use FastAPI as the HTTP API framework.

FastAPI is restricted to the transport layer. Application, synchronization, analytics, and persistence logic must remain framework-independent.

---

### D-011 — Direct PyMongo Usage

**Decision:** Use the official PyMongo driver directly, preferably through its asynchronous API.

Do not use an ODM in the MVP. MongoDB-specific behavior should remain explicit, while PyMongo access is isolated behind repository/data-access abstractions.

---

### D-012 — Synchronous MVP Synchronization

**Decision:** Repository synchronization runs synchronously inside the API request in the MVP.

Synchronization is bounded by configurable import limits and only one sync may run per repository at a time.

The synchronization service must remain independent from FastAPI so the same logic can later be executed by a background worker.

---

### D-013 — Incremental Synchronization Strategy

**Decision:** Use independent resource-level `updated_at` checkpoints for pull requests and issues. Writes are idempotent upserts, and checkpoints advance only after a complete successful resource synchronization.

Interrupted runs safely replay data from the previous successful checkpoint instead of persisting fragile pagination state.

---

### D-014 — GitHub Rate-Limit and Retry Strategy

**Decision:** Use authenticated GitHub API requests, serial execution in the MVP, rate-limit header monitoring, bounded exponential backoff, finite retries, and conditional requests where useful.

---

### D-015 — GitHub REST API for MVP

**Decision:** Use GitHub REST API for the MVP.

GraphQL is deferred as a later comparison or optimization exercise rather than included in the initial implementation.

---

### D-016 — Application API Authentication

**Decision:** The MVP will not implement user accounts or JWT authentication.

Local development may run without authentication. Public deployments should protect write and synchronization endpoints with a simple API key supplied through configuration, while read-only analytics endpoints may remain public.

---

### D-017 — Typed Configuration and Secret Management

**Decision:** Use `pydantic-settings` for centralized typed configuration.

Configuration is supplied through environment variables. Local development may use `.env`; `.env.example` is committed for documentation. GitHub tokens, API keys, and credential-bearing MongoDB URIs must never be committed.

---

### D-018 — Layered Testing Strategy

**Decision:** Use layered testing with unit tests, GitHub-client tests using mocked HTTP transport, real MongoDB integration tests through Testcontainers, FastAPI API tests, explicit failure-path tests, and a small number of end-to-end smoke tests.

Target approximately 80% overall code coverage as a guideline, with priority given to critical business logic and failure scenarios rather than maximizing the percentage.

---



---

---

---

### D-019 — Local Development Environment

**Decision:** Run FastAPI directly on the developer host in an isolated Python environment and run MongoDB through Docker Compose with a persistent development volume.

Integration tests use a separate Testcontainers-managed MongoDB instance. Mongo Express is optional. Containerizing the application itself is deferred until the application is stable.

---

### D-020 — Python Project and Dependency Management

**Decision:** Use `uv` for Python project, dependency, virtual-environment, and lockfile management.

Dependencies are declared in `pyproject.toml`; `uv.lock` is committed for reproducibility; `.venv/` remains local and uncommitted. Runtime and development dependencies are managed separately.

---

### D-021 — Code Quality Tooling

**Decision:** Use Ruff for linting and formatting, mypy for static type checking, pytest for tests, and pre-commit for fast local quality checks.

Black is intentionally omitted because Ruff formatter provides the formatting layer. The project's own code starts from a strict mypy posture, with only targeted exceptions for third-party typing limitations.

---

### D-022 — GitHub Actions CI

**Decision:** Use GitHub Actions on pull requests and pushes to `main`, with parallel `quality` and `test` jobs.

The quality job runs Ruff linting, Ruff formatting checks, and mypy. The test job runs the complete pytest suite, Testcontainers-based MongoDB integration tests, smoke tests, and coverage reporting.

Docker image building and deployment are not part of the MVP CI pipeline.

---

### D-023 — MVP Observability

**Decision:** Use structured logging, request/correlation IDs, synchronization lifecycle events, `/health`, `/ready`, operational sync measurements in logs, and centralized typed exception handling.

Prometheus, Grafana, OpenTelemetry, and a dedicated metrics endpoint are deferred.

---

### D-024 — Backend-Only MVP

**Decision:** The MVP is backend/API-only.

FastAPI Swagger/OpenAPI documentation is the interactive interface. A separate frontend or analytics dashboard is deferred unless it later adds clear portfolio value.

---

### D-025 — Public Cloud Deployment

**Decision:** Deploy the portfolio MVP on Google Cloud Run with a MongoDB Atlas Free cluster, preferably on GCP.

Cloud Run should scale to zero with a low maximum instance count. Read-only analytics and API documentation may be public, while write/synchronization endpoints remain API-key protected.

The deployment is explicitly designed to remain within free-tier limits, with billing alerts and conservative resource constraints.

---

### D-026 — Post-MVP AI Extension

**Decision:** After the core MVP is complete, add semantic search over GitHub issues and pull requests using an application-level `EmbeddingService` and MongoDB Vector Search.

Issue/PR text is added to the stored model only when required by the AI use case. A later RAG layer may answer repository-engineering questions with explicit source references.

LangChain and similar orchestration frameworks are intentionally deferred for the first implementation.

---

## 7. Open Design Questions

Each question should remain here until resolved.

When a decision is made:

1. Replace `OPEN` with `DECIDED`.
2. Write the answer directly under the question.
3. Add the resulting decision to **Confirmed Decisions** if it has architectural significance.
4. Update the roadmap when necessary.

---

### Q-001 — Which analytics questions should the MVP answer?

**Status:** DECIDED

The MVP will implement the following seven analytics areas:

1. **Pull request lead time**  
   Time from pull request creation to merge.

2. **Time to first review**  
   Time from pull request creation to the first submitted review.

3. **Pull request size statistics**  
   Analysis based on changed files, additions, and deletions.

4. **Pull request size vs. review time**  
   Analyze whether larger pull requests tend to take longer to review.

5. **Contributor activity**  
   Activity based on commits, pull requests, and reviews.

6. **Issue resolution time**  
   Time from issue creation to closure.

7. **Repository activity trends over time**  
   Weekly/monthly trends for pull requests and issues.

**Decision:** These seven metrics are sufficient for the MVP.

**Rationale:**  
The goal is not to maximize the number of metrics, but to demonstrate different backend and MongoDB concerns: temporal analysis, aggregation, document relationships, trend analysis, indexing, and non-trivial query pipelines.

Potential future analytics such as backlog evolution, merge-rate dashboards, release analytics, bus-factor-like indicators, and advanced contributor concentration are deferred until after the MVP.

---

### Q-002 — Which GitHub entities should be stored?

**Status:** DECIDED

The MVP will persist the following top-level collections:

- `repositories`
- `pull_requests`
- `issues`
- `sync_states`

The following data will be embedded inside pull request documents:

- `reviews[]`
- `commits[]`

The following will **not** be stored as separate collections in the MVP:

- Users / contributors
- Labels
- Releases
- Branches
- Review comments
- Changed-file details
- Commits

Small user identity snapshots will be embedded where needed, for example:

```json
{
  "github_id": 12345,
  "login": "developer1"
}
```

**Commit modeling decision:**

Pull-request commits are treated as part of the pull request aggregate and are embedded in `pull_requests.commits[]`.

A separate repository-level `commits` collection will not be created for the MVP.

**Rationale:**

For the selected analytics use cases, commits are primarily useful in the context of a pull request. Embedding them allows direct analysis of:

- commits per pull request,
- average commits per pull request,
- commit-count distribution,
- pull request size vs. commit count,
- commit count vs. review time.

This keeps the MongoDB model aligned with the actual analytical aggregate instead of reproducing the GitHub API resource model.

Repository-level commit activity is therefore removed from the MVP analytics scope.

**Decision:** Store repository, pull request, issue, and sync-state documents as top-level collections. Embed reviews and commits in pull requests. Do not create a separate commits collection.

---

### Q-003 — What should the MongoDB document model look like?

**Status:** DECIDED

The MVP uses four top-level collections:

- `repositories`
- `pull_requests`
- `issues`
- `sync_states`

Pull request reviews and commits are embedded in pull request documents.

Derived analytics values are calculated at query time rather than persisted unless later performance measurements justify denormalization.

---

#### `repositories`

Example:

```json
{
  "_id": "ObjectId",
  "github_id": 123456,
  "owner": "spring-projects",
  "name": "spring-boot",
  "full_name": "spring-projects/spring-boot",
  "default_branch": "main",
  "html_url": "https://github.com/spring-projects/spring-boot",
  "github_created_at": "datetime",
  "github_updated_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

Indexes:

```javascript
{ github_id: 1 } // unique
{ full_name: 1 } // unique
```

`full_name` is retained as a natural repository identifier for API use and human readability.

---

#### `pull_requests`

Example:

```json
{
  "_id": "ObjectId",
  "repository_id": "ObjectId",
  "github_id": 1234567,
  "number": 19234,
  "title": "Fix transaction handling",
  "author": {
    "github_id": 1234,
    "login": "developer1"
  },
  "state": "closed",
  "draft": false,
  "created_at": "datetime",
  "updated_at": "datetime",
  "closed_at": "datetime|null",
  "merged_at": "datetime|null",
  "additions": 130,
  "deletions": 42,
  "changed_files": 8,
  "base_branch": "main",
  "commits": [
    {
      "sha": "abc123",
      "author": {
        "github_id": 1234,
        "login": "developer1",
        "name": "Developer Name"
      },
      "committed_at": "datetime"
    }
  ],
  "reviews": [
    {
      "github_id": 98765,
      "reviewer": {
        "github_id": 5678,
        "login": "reviewer1"
      },
      "state": "APPROVED",
      "submitted_at": "datetime"
    }
  ]
}
```

Recommended indexes:

```javascript
{ repository_id: 1, number: 1 } // unique
{ repository_id: 1, created_at: 1 }
{ repository_id: 1, merged_at: 1 }
{ repository_id: 1, "author.github_id": 1 }
```

Additional indexes on embedded review or commit fields should only be added after measuring real query patterns.

---

#### Embedded `reviews[]`

Store only data required for analytics:

```json
{
  "github_id": 98765,
  "reviewer": {
    "github_id": 5678,
    "login": "reviewer1"
  },
  "state": "APPROVED",
  "submitted_at": "datetime"
}
```

Do not persist review bodies, URLs, permissions, avatar URLs, or unrelated GitHub payload fields in the MVP.

Reviews are embedded because their lifecycle and analytics usage are tightly coupled to their pull request.

---

#### Embedded `commits[]`

Example:

```json
{
  "sha": "abcdef123",
  "author": {
    "github_id": 1234,
    "login": "developer1",
    "name": "Developer Name"
  },
  "committed_at": "datetime"
}
```

`github_id` and `login` may be `null` because not every Git commit author can be mapped to a GitHub account.

Email addresses are intentionally not persisted because they are not required by the MVP analytics.

Commits are embedded because the selected use cases analyze commits mainly in the context of a pull request.

---

#### `issues`

Example:

```json
{
  "_id": "ObjectId",
  "repository_id": "ObjectId",
  "github_id": 827364,
  "number": 4382,
  "title": "Application fails during startup",
  "author": {
    "github_id": 12345,
    "login": "developer2"
  },
  "state": "closed",
  "created_at": "datetime",
  "updated_at": "datetime",
  "closed_at": "datetime|null"
}
```

Recommended indexes:

```javascript
{ repository_id: 1, number: 1 } // unique
{ repository_id: 1, created_at: 1 }
{ repository_id: 1, closed_at: 1 }
{ repository_id: 1, "author.github_id": 1 }
```

The MVP intentionally does not persist:

- body
- comments
- labels
- assignees
- milestone
- reactions

These fields are not required by the selected analytics.

---

#### `sync_states`

Synchronization state is stored per repository and resource type.

Example:

```json
{
  "_id": "ObjectId",
  "repository_id": "ObjectId",
  "resource": "pull_requests",
  "status": "completed",
  "last_started_at": "datetime",
  "last_completed_at": "datetime",
  "checkpoint": {
    "updated_since": "datetime"
  },
  "processed_count": 487,
  "last_error": null
}
```

Recommended unique index:

```javascript
{ repository_id: 1, resource: 1 }
```

This allows pull request and issue synchronization to fail, retry, and recover independently.

---

#### Derived values

The MVP will calculate derived analytics values instead of persisting them.

Examples:

- pull request lead time
- time to first review
- review duration
- commit count
- issue resolution time

For example, commit count can be calculated using:

```javascript
{ $size: "$commits" }
```

Denormalized derived fields may be added later only if profiling shows a measurable performance benefit.

---

#### Multikey index constraint

Both `commits[]` and `reviews[]` are arrays.

MongoDB compound multikey indexes cannot index multiple independent array fields from the same document in a single compound index.

Therefore, the design must avoid indexes such as:

```javascript
{
  "commits.author.github_id": 1,
  "reviews.reviewer.github_id": 1
}
```

This is an accepted trade-off of embedding both collections inside the pull request aggregate.

---

#### Logical document model

```text
repositories
    |
    +-------------------+
    |                   |
    v                   v
pull_requests         issues
    |
    +-- commits[]
    |
    +-- reviews[]

repositories
    |
    v
sync_states
```

**Decision:** Use document-oriented aggregates centered on pull requests rather than reproducing the GitHub API resource model or a normalized SQL-style schema.

---

### Q-004 — Which MongoDB features should the project intentionally demonstrate?

**Status:** DECIDED

The MVP will intentionally demonstrate the following MongoDB capabilities because they directly support the selected use cases.

#### Core analytics features

- Aggregation pipelines
- `$match`
- `$project`
- `$group`
- `$unwind`
- MongoDB date operators
- `$facet`

These form the primary analytics mechanism of the application.

#### Indexing and performance

- Compound indexes
- Multikey indexes where justified by real query patterns
- `explain()` and query-plan analysis

Indexes should be designed around repository-scoped access patterns and validated through actual query plans rather than added speculatively.

#### Data ingestion and synchronization

- Bulk writes
- Upserts

These are required for efficient, idempotent GitHub data synchronization.

#### Data integrity

- MongoDB schema validation

MongoDB's flexible document model will be used intentionally, while schema validation protects required structure and data quality.

#### Explicitly deferred for the MVP

The following MongoDB features are not part of the MVP unless a concrete requirement appears later:

- `$lookup`
- Change streams
- TTL indexes
- Text search
- Time-series collections
- Window functions

Window functions may become useful later for rolling averages, smoothing, or more advanced trend analytics.

`$lookup` is intentionally not required in the MVP because pull request reviews and commits are embedded in the pull request aggregate.

#### Feature-to-use-case mapping

| Use case | MongoDB capability |
|---|---|
| Pull request lead time | `$match`, `$project`, date operators |
| Time to first review | `$unwind`, `$group`, date operators |
| Pull request size statistics | `$group`, `$avg`, `$min`, `$max` |
| Pull request size vs. review time | `$project`, `$unwind`, aggregation pipeline |
| Contributor activity | `$unwind`, `$group` |
| Issue resolution time | Date operators, `$group` |
| Repository activity trends | Date grouping |
| Repository overview endpoint | `$facet` |
| Import / synchronization | Bulk writes, upserts |
| Query performance | Compound/multikey indexes, `explain()` |
| Data integrity | Schema validation |

**Decision:** Use aggregation pipelines as the main analytics mechanism, supported by compound and selective multikey indexes, bulk upserts, schema validation, and query-plan analysis. Use `$facet` and `$unwind` where naturally required. Defer advanced MongoDB features that do not yet solve a concrete project requirement.

---

### Q-005 — Which Python web framework should be used?

**Status:** DECIDED

**Decision:** Use FastAPI as the HTTP API framework.

**Rationale:**

FastAPI fits the project because it provides:

- strong integration with Python type hints,
- native asynchronous request handling,
- automatic OpenAPI documentation,
- lightweight API-centric architecture,
- good testability,
- minimal framework overhead compared with a full-stack framework.

FastAPI will be limited to the API / transport layer.

Business logic, synchronization, persistence, and analytics logic must remain independent from FastAPI.

Target layering:

```text
FastAPI
   |
   v
Application / Service layer
   |
   +---------> GitHub client
   |
   +---------> Repository layer
   |                |
   |                v
   |             MongoDB
   |
   +---------> Analytics layer
```

This keeps the framework replaceable and prevents HTTP concerns from leaking into domain or persistence logic.

---

### Q-006 — Which MongoDB Python driver / abstraction layer should be used?

**Status:** DECIDED

**Decision:** Use the official PyMongo driver directly instead of an ODM.

Prefer the asynchronous PyMongo API so MongoDB access integrates naturally with FastAPI and other async I/O.

**Rationale:**

MongoDB itself is a core technology being demonstrated by this project. Using PyMongo directly keeps the following concepts explicit and visible:

- collections,
- document shapes,
- indexes,
- aggregation pipelines,
- bulk writes,
- upserts,
- schema validation,
- query-plan analysis with `explain()`.

An ODM such as Beanie, ODMantic, or MongoEngine would hide part of the MongoDB-specific design that the project is intended to demonstrate.

Persistence details must still be isolated behind a repository/data-access layer so application services do not depend directly on PyMongo.

Target dependency direction:

```text
FastAPI
  |
Service layer
  |
Repository layer
  |
PyMongo
  |
MongoDB
```

An ODM should only be introduced later if a concrete maintainability problem justifies it.

---

### Q-007 — Sync architecture: synchronous request, background job, or both?

**Status:** DECIDED

**Decision:** The MVP will execute repository synchronization synchronously within the API request.

Example flow:

```text
POST /repositories/{id}/sync
        |
        v
RepositorySyncService
        |
        +--> GitHub API
        |
        +--> MongoDB bulk upserts
        |
        v
HTTP response with sync summary
```

**Constraints:**

- Synchronization volume must be deliberately bounded.
- Import limits must be configurable.
- A repository must not have multiple concurrent synchronization processes.
- The synchronization service must be independent from FastAPI.
- The implementation must remain easy to move to a background worker later.

Initial working limits are approximately:

- up to 500 pull requests,
- up to 500 issues,
- associated reviews and commits required by those pull requests.

Exact limits may be adjusted after measuring GitHub API behavior and request duration.

**Rationale:**

A synchronous request keeps the MVP architecture simple and avoids introducing queues, workers, schedulers, and job orchestration before they solve a real problem.

At the same time, synchronization logic remains in an application service rather than the endpoint itself so it can later be invoked by a background worker without redesigning the core logic.

---

### Q-008 — How should incremental synchronization work?

**Status:** DECIDED

**Decision:** Incremental synchronization will use resource-specific checkpoints stored in `sync_states`.

Pull requests and issues will have independent synchronization state.

#### Issues

Use the GitHub REST API `since` filtering semantics based on resource update timestamps.

The persisted checkpoint stores the latest successfully completed `updated_at` boundary.

#### Pull requests

The pull request API does not provide the same direct `since` filtering model.

Pull requests will therefore be requested ordered by update time, newest first, and pagination will continue until the previously completed `updated_at` checkpoint is reached.

#### Pagination

Follow GitHub pagination links returned by the API.

Pagination position itself is temporary execution state and is **not** persisted as the long-term checkpoint.

The durable checkpoint is based on resource update time.

#### Writes

All persistence during synchronization must be idempotent.

Use upserts based on repository-scoped GitHub identifiers so that replaying already processed items is safe.

#### Checkpoint advancement

A resource checkpoint is advanced only after the complete synchronization of that resource succeeds.

If a synchronization fails:

- the previous successful checkpoint remains active,
- the next run may reprocess already seen records,
- idempotent upserts prevent duplicates.

#### Pull request child data

When a pull request is detected as new or updated, its embedded:

- `reviews[]`
- `commits[]`

are fetched again and rebuilt from the source data.

This keeps the pull request aggregate internally consistent.

#### Restartability

The synchronization design intentionally prefers safe replay over fragile page-level resume state.

**Decision summary:** Persist resource-level `updated_at` checkpoints, use idempotent upserts, advance checkpoints only after full resource success, and allow safe replay after interruption.

---

### Q-009 — How should GitHub API rate limiting be handled?

**Status:** DECIDED

**Decision:** Use authenticated GitHub REST API requests and apply bounded retry/backoff behavior.

#### Authentication

Even for public repositories, GitHub API access should be authenticated through a configured token.

#### Rate-limit monitoring

Inspect relevant GitHub rate-limit headers on responses, including:

- `x-ratelimit-remaining`
- `x-ratelimit-reset`
- `retry-after` when present

#### Request concurrency

The MVP will execute GitHub API requests serially.

Parallel request fan-out is intentionally deferred to reduce complexity and lower the risk of secondary rate limiting.

#### Retry strategy

For transient network failures and retryable server errors:

- use bounded exponential backoff,
- use a finite retry budget,
- fail the synchronization cleanly after retries are exhausted.

Example progression:

```text
1s -> 2s -> 4s -> ...
```

The exact values remain implementation details and should be configurable where useful.

#### Rate-limit handling

- If `Retry-After` is provided, respect it.
- If the primary rate limit is exhausted, wait until the reset boundary rather than blindly retrying.
- Secondary-rate-limit responses use a bounded backoff strategy.
- Never retry indefinitely.

#### Conditional requests

Use conditional requests such as `ETag` / `If-None-Match` where they provide measurable value and simplify repeated reads.

They are an optimization, not a mandatory requirement for every endpoint.

**Decision summary:** Authenticated requests, serial execution, explicit rate-limit awareness, bounded exponential backoff, finite retries, and conditional requests where useful.

---

### Q-010 — GitHub REST API or GraphQL API?

**Status:** DECIDED

**Decision:** Use the GitHub REST API for the MVP.

**Rationale:**

REST is preferred initially because it:

- keeps the first synchronization implementation simpler,
- maps clearly to the selected entities,
- is easier to debug,
- fits the existing pagination, checkpoint, retry, and rate-limit strategy,
- reduces implementation risk while Python and MongoDB remain the main learning/demo focus.

GraphQL is explicitly deferred rather than rejected.

A later phase may reimplement or supplement one import/analytics path with GitHub GraphQL and compare:

- number of requests,
- payload size,
- pagination complexity,
- rate-limit behavior,
- implementation complexity,
- maintainability.

This comparison may become a useful portfolio extension because it demonstrates architectural trade-off analysis rather than simply adding another technology.

**Decision summary:** REST for the MVP; GraphQL reserved for a later comparison/optimization exercise.

---

### Q-011 — Authentication model for the application API

**Status:** DECIDED

**Decision:** The MVP will not implement user accounts, JWT-based authentication, or a full authorization subsystem.

#### Local development

Local development and automated tests may run without application-level authentication.

#### Public deployment

If the application is deployed publicly:

- write and synchronization endpoints must be protected with a simple API key,
- read-only analytics endpoints may remain public,
- the API key is supplied through configuration and never committed to version control.

Examples of protected endpoints:

```text
POST /repositories
POST /repositories/{id}/sync
```

Examples of potentially public endpoints:

```text
GET /repositories
GET /repositories/{id}
GET /repositories/{id}/analytics/...
```

**Rationale:**

Full user authentication would add substantial implementation scope without contributing meaningfully to the project's primary goals of demonstrating Python, MongoDB, backend architecture, synchronization, and analytics.

**Decision summary:** No user/JWT authentication in the MVP. Use optional API-key protection for write/sync endpoints in public deployments.

---

### Q-012 — Configuration and secrets

**Status:** DECIDED

**Decision:** Use `pydantic-settings` as the centralized, typed configuration layer.

Configuration is provided through environment variables. Local development may use a `.env` file. The repository will contain a `.env.example` file documenting supported configuration values without secrets.

Example settings:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_database: str = "github_analytics"
    github_token: str
    api_key: str | None = None
    max_pull_requests: int = 500
    max_issues: int = 500
    github_retry_count: int = 4
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
```

Expected local configuration:

```text
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=github_analytics
GITHUB_TOKEN=
API_KEY=
MAX_PULL_REQUESTS=500
MAX_ISSUES=500
GITHUB_RETRY_COUNT=4
LOG_LEVEL=INFO
```

#### Secrets

Treat the following as secrets:

- `GITHUB_TOKEN`
- `API_KEY`
- credential-bearing `MONGODB_URI`

These values must never be committed to version control.

#### Non-secret configuration

Examples:

- `MONGODB_DATABASE`
- `MAX_PULL_REQUESTS`
- `MAX_ISSUES`
- `GITHUB_RETRY_COUNT`
- `LOG_LEVEL`

#### Application access

Application code must access configuration through the centralized `Settings` abstraction. Direct environment access such as `os.getenv("GITHUB_TOKEN")` should not be scattered across the codebase.

A cached settings provider may be used:

```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

**Decision summary:** Typed centralized configuration via `pydantic-settings`, environment variables in all environments, optional `.env` locally, `.env.example` committed, and no secrets in version control.

---

### Q-013 — Testing strategy

**Status:** DECIDED

**Decision:** Use a layered testing strategy with unit, GitHub-client, MongoDB integration, FastAPI API, failure-path, and limited end-to-end tests.

#### Unit tests

Use unit tests for application/service logic.

Unit tests should:

- avoid real MongoDB,
- avoid real GitHub API calls,
- mock repository/data-access abstractions where appropriate,
- mock the `GitHubClient` at the service boundary,
- focus on business rules and synchronization behavior.

#### GitHub client tests

Test the GitHub client using mocked HTTP responses at the transport boundary.

These tests should cover:

- response parsing,
- pagination,
- rate-limit headers,
- retry/backoff behavior,
- error mapping,
- malformed or unexpected responses,
- retry exhaustion.

The GitHub API itself must not be called during automated tests.

#### MongoDB integration tests

MongoDB-specific behavior must be tested against a real MongoDB instance rather than a MongoDB mock.

Use **Testcontainers** to start an isolated MongoDB container for integration tests.

Integration tests should cover:

- indexes,
- unique constraints,
- schema validation,
- aggregation pipelines,
- bulk writes,
- upserts,
- multikey behavior,
- idempotent persistence.

A mock such as `mongomock` is not sufficient for these tests because the project intentionally demonstrates real MongoDB behavior.

#### FastAPI API tests

Use API tests to verify:

- routing,
- request validation,
- response models,
- HTTP status codes,
- dependency wiring,
- API-key behavior where enabled,
- error responses.

#### Failure-path tests

Failure scenarios are first-class test cases.

Important cases include:

- interrupted synchronization,
- GitHub 5xx responses,
- GitHub rate-limit exhaustion,
- retry exhaustion,
- repeated imports,
- duplicate prevention,
- checkpoint advancement only after successful synchronization,
- refresh of embedded reviews and commits,
- invalid API input.

#### End-to-end tests

Include only a small number of end-to-end smoke tests.

The MVP does not need a large E2E suite.

#### Coverage

Target approximately **80% overall code coverage** as a useful quality signal.

Coverage is not an absolute objective. Critical business logic and failure paths are more important than maximizing the percentage.

Coverage should be measured in CI.

#### Planned testing tools

Expected tools include:

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- Testcontainers for Python
- an HTTP mocking library compatible with the selected GitHub HTTP client

The exact HTTP client and mocking library will be selected during implementation.

#### Proposed test structure

```text
tests/
├── unit/
│   ├── services/
│   └── analytics/
├── integration/
│   ├── persistence/
│   └── mongodb/
├── api/
│   └── test_repositories.py
├── github/
│   └── test_client.py
└── e2e/
    └── test_sync_smoke.py
```

**Decision summary:** Use layered tests, real MongoDB through Testcontainers for integration testing, mocked GitHub HTTP transport, explicit failure-path coverage, limited E2E smoke tests, and approximately 80% overall coverage as a guideline rather than a hard target.

---

### Q-014 — Local development environment

**Status:** DECIDED

**Decision:** Run the Python/FastAPI application directly on the developer host inside an isolated Python environment, while MongoDB runs in Docker Compose.

Target development setup:

```text
Host machine
├── Python virtual environment
├── FastAPI application
├── IDE / debugger
└── Docker Compose
    └── MongoDB
```

#### FastAPI application

During normal development, run the application directly on the host rather than inside Docker.

Example:

```text
uvicorn github_analytics.main:app --reload
```

This keeps the development and debugging cycle fast and IDE-friendly.

#### MongoDB

Run MongoDB through Docker Compose with a persistent development volume.

Initial example:

```yaml
services:
  mongodb:
    image: mongo:8
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
```

The exact MongoDB image should later be pinned to a concrete version for reproducibility.

#### Python environment

Use an isolated Python environment for all project dependencies.

The exact package/dependency manager (`uv`, Poetry, or pip-based tooling) will be decided in Q-015.

#### MongoDB GUI

Mongo Express is optional and is not part of the default development stack.

A separate desktop tool such as MongoDB Compass may be used when visual inspection is useful.

#### Integration tests

Integration tests must not reuse the normal development MongoDB instance.

They will start their own isolated MongoDB instance through Testcontainers.

Therefore:

```text
Development MongoDB
    !=
Integration-test MongoDB
```

This keeps tests reproducible and prevents test data from affecting the developer database.

#### Application containerization

Containerizing the FastAPI application itself is deferred until the application is sufficiently stable.

Initial development:

```text
FastAPI -> host
MongoDB -> Docker
```

Later:

```text
Docker Compose
├── application
└── mongodb
```

**Decision summary:** Host-run FastAPI, Docker Compose MongoDB with persistent volume, Testcontainers for isolated integration-test MongoDB, optional MongoDB GUI, and deferred application containerization.

---

### Q-015 — Packaging and dependency management

**Status:** DECIDED

**Decision:** Use `uv` for Python project management, dependency management, virtual-environment management, and lockfile generation.

#### Project metadata and dependencies

Declare project metadata and dependencies in:

```text
pyproject.toml
```

Use `uv` commands to manage dependencies rather than editing generated lock data manually.

Examples:

```bash
uv add fastapi
uv add pymongo
uv add --dev pytest
uv add --dev pytest-asyncio
uv add --dev pytest-cov
```

#### Virtual environment

Use the project-local virtual environment created/managed by `uv`:

```text
.venv/
```

The virtual environment is local development state and must not be committed.

#### Lockfile

Commit:

```text
uv.lock
```

to version control.

This provides a reproducible dependency graph across developer machines and CI.

#### Python version

Use a project-level Python version declaration, for example:

```text
.python-version
```

The exact supported Python version will be selected during project initialization.

#### Typical workflow

```bash
uv sync
uv run uvicorn github_analytics.main:app --reload
uv run pytest
```

#### Dependency groups

Keep runtime and development dependencies separate.

Examples of development-only dependencies include:

- pytest
- pytest-asyncio
- pytest-cov
- Testcontainers
- Ruff
- mypy
- pre-commit

The exact code-quality tool set will be decided in Q-016.

#### Alternatives not selected

Poetry and pip/requirements-based workflows are not used in the MVP.

They remain valid Python tooling choices, but `uv` provides a simpler unified workflow for this application-oriented project.

**Decision summary:** Use `uv`, `pyproject.toml`, committed `uv.lock`, a project-local `.venv`, and separate runtime/development dependencies.

---

### Q-016 — Code quality tooling

**Status:** DECIDED

**Decision:** Use Ruff for linting and formatting, mypy for static type checking, pytest for testing, and pre-commit for fast local quality checks.

Black will not be used separately.

#### Ruff

Use Ruff for:

- linting,
- import-related checks,
- common bug-prone patterns,
- formatting.

Ruff formatter replaces Black in this project to avoid redundant formatting tools.

Configuration belongs in `pyproject.toml`.

The initial lint rule set should be intentionally useful rather than maximally broad.

Avoid enabling rule groups that conflict with the formatter or create large amounts of low-value noise.

#### mypy

Use mypy for static type checking.

Because this is a greenfield project, start from a strict typing posture for the project's own code.

If third-party libraries have incomplete or incompatible typing, relax checks only in narrowly scoped configuration sections rather than globally weakening the project.

#### pytest

Use pytest as the main test runner.

Testing strategy and test layers are defined separately in Q-013.

#### pre-commit

Use pre-commit for fast local checks before commits.

Planned checks:

```text
ruff check --fix
ruff format
mypy
```

The pre-commit workflow should remain fast.

Do not run the full integration and Testcontainers test suite on every local commit.

#### CI responsibility

The complete test suite belongs in CI, including:

- unit tests,
- API tests,
- GitHub client tests,
- MongoDB integration tests,
- coverage reporting.

Local pre-commit checks and CI checks must be complementary rather than duplicates of the entire pipeline.

**Decision summary:** Ruff handles linting and formatting, mypy handles strict static typing, pytest handles tests, and pre-commit provides fast local quality gates. Black is not used separately.

---

### Q-017 — CI/CD

**Status:** DECIDED

**Decision:** Use GitHub Actions for continuous integration on pull requests and pushes to `main`.

The MVP CI pipeline will use two parallel jobs:

```text
Push / Pull Request
        |
        +--------------------+
        |                    |
        v                    v
     QUALITY               TEST
```

#### Triggers

Run CI on:

- pull requests,
- pushes to `main`.

#### Quality job

The quality job should remain fast and should not require MongoDB.

Planned steps:

```text
checkout
setup uv / Python
uv sync --locked
ruff check
ruff format --check
mypy
```

Representative commands:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

#### Test job

The test job runs the complete automated test suite:

- unit tests,
- FastAPI API tests,
- GitHub client tests,
- MongoDB integration tests through Testcontainers,
- limited end-to-end smoke tests,
- coverage reporting.

Representative command:

```bash
uv run pytest --cov=github_analytics --cov-report=term-missing
```

#### Job execution model

Run `quality` and `test` in parallel rather than making one depend on the other.

This provides faster and more complete feedback from a single workflow run.

#### Python and dependency reproducibility

Use the project's pinned Python version and committed `uv.lock`.

CI installs dependencies with:

```bash
uv sync --locked
```

The project should use the official/recommended `uv` GitHub Actions setup.

#### Coverage

Coverage is reported in CI.

The approximately 80% target remains a guideline and is not initially enforced with a hard `--cov-fail-under` threshold.

Critical business logic and failure-path coverage remain more important than the raw percentage.

#### Docker image build

Do not build the application Docker image in the MVP CI pipeline.

Application containerization remains deferred.

#### Deployment

The MVP CI workflow does not perform deployment.

Deployment will be decided separately in Q-020.

**Decision summary:** GitHub Actions runs parallel quality and test jobs on pull requests and pushes to `main`, using locked `uv` dependencies and the pinned Python version. Docker image build and deployment remain deferred.

---

### Q-018 — Observability

**Status:** DECIDED

**Decision:** Use structured application logging with request/correlation IDs, explicit synchronization lifecycle events, health/readiness endpoints, operational sync metrics in logs, and centralized exception handling.

#### Structured logging

Operational logs should contain structured fields rather than relying only on free-form messages.

Example:

```json
{
  "event": "repository_sync_failed",
  "repository": "spring-projects/spring-boot",
  "resource": "pull_requests",
  "request_id": "c91f...",
  "processed_count": 183,
  "retry_count": 3,
  "duration_ms": 8241,
  "error_type": "GitHubRateLimitError"
}
```

#### Request / correlation ID

Every incoming API request should have a request/correlation ID.

Use an incoming `X-Request-ID` when appropriate or generate one when missing.

The ID should propagate through:

```text
FastAPI request
    |
    v
Application / Service layer
    |
    +--> GitHub client
    |
    +--> Persistence
```

and appear in related logs.

#### Synchronization lifecycle events

Important sync events include:

- `sync_started`
- `sync_completed`
- `sync_failed`
- `github_request_retry`
- `github_rate_limit_hit`
- `checkpoint_updated`

Useful fields include:

- repository ID/name,
- resource,
- processed count,
- created count,
- updated count,
- duration,
- retry count,
- request ID.

#### Health endpoint

Provide:

```text
GET /health
```

This indicates that the application process is running.

Example response:

```json
{
  "status": "ok"
}
```

#### Readiness endpoint

Provide:

```text
GET /ready
```

Readiness should verify MongoDB connectivity.

Do not call GitHub from the readiness check because GitHub is an external dependency and repeated readiness checks should not consume API capacity or create false application unavailability.

#### Operational metrics

Log useful operational values such as:

- synchronization duration,
- processed item counts,
- GitHub request counts,
- retry counts,
- failure counts.

These values may later become dedicated monitoring metrics.

#### Exception handling

Use typed application/domain exceptions and centralized FastAPI exception mapping.

Examples:

- `RepositoryNotFoundError`
- `GitHubRateLimitError`
- `GitHubApiError`
- `SynchronizationAlreadyRunningError`
- `SynchronizationFailedError`

Avoid repeated broad `try/except` blocks in individual API endpoints.

#### Deferred observability tooling

The following are deferred until a concrete deployment/monitoring need exists:

- Prometheus,
- Grafana,
- OpenTelemetry,
- dedicated `/metrics` endpoint.

**Decision summary:** Structured logging, correlation IDs, sync lifecycle logging, `/health`, `/ready`, operational values in logs, and centralized exception handling are part of the MVP. Full metrics/tracing stacks are deferred.

---

### Q-019 — Should the application have a UI?

**Status:** DECIDED

**Decision:** The MVP will be backend/API-only.

FastAPI's generated interactive API documentation will serve as the primary UI for development, demonstration, and manual exploration.

Expected interfaces:

```text
FastAPI backend
├── REST API
├── /docs      -> Swagger UI
├── /redoc     -> ReDoc
├── /health
└── /ready
```

#### Rationale

The project's primary goals are to demonstrate:

- Python backend engineering,
- MongoDB data modeling,
- GitHub API integration,
- synchronization,
- analytics,
- testing,
- observability.

A separate frontend would add implementation scope in a different technology area without materially improving the core backend demonstration.

#### Portfolio presentation

The README may include:

- example API requests,
- example analytics responses,
- selected Swagger/OpenAPI screenshots,
- architecture diagrams.

#### Future dashboard

A small analytics dashboard may be added later if it materially improves portfolio presentation.

Possible future content:

```text
Repository selector
        |
        +--> PR lead time
        +--> review time
        +--> issue resolution
        +--> contributor activity
```

A separate frontend is not part of the MVP.

**Decision summary:** Backend/API-only MVP using FastAPI Swagger/OpenAPI documentation as the interactive interface. A standalone frontend/dashboard is deferred.

---

### Q-020 — Deployment target

**Status:** DECIDED

**Decision:** Deploy the portfolio MVP publicly on Google Cloud Run and use a MongoDB Atlas Free cluster, preferably hosted on GCP.

Target deployment:

```text
Internet
   |
   v
Google Cloud Run
   |
   |-- FastAPI
   |-- Swagger/OpenAPI
   |-- /health
   |-- /ready
   |
   +----> GitHub REST API
   |
   +----> MongoDB Atlas Free cluster
```

#### Cost objective

The deployment must be designed to stay within the free tiers of commercial cloud providers.

The project should use paid commercial cloud platforms, but the intended operating cost for the portfolio workload is:

```text
0 EUR
```

This is a target rather than an absolute guarantee because free-tier limits can be exceeded.

#### Google Cloud Run

Use Google Cloud Run for the FastAPI application.

Recommended settings:

```text
min instances = 0
max instances = 1
```

This allows scale-to-zero when unused and limits accidental cost growth.

The Cloud Run request timeout may be configured high enough to support the current synchronous repository synchronization model.

#### MongoDB Atlas

Use a MongoDB Atlas Free cluster.

Prefer a GCP-backed Atlas region when practical so the application and database remain on the same cloud provider and can be placed geographically close to each other.

#### Public access model

Read-only endpoints may be publicly accessible:

```text
GET /repositories
GET /repositories/{id}
GET /repositories/{id}/analytics/...
GET /docs
GET /redoc
GET /health
GET /ready
```

Write and synchronization endpoints remain protected with the configured API key:

```text
POST /repositories
POST /repositories/{id}/sync
```

This allows LinkedIn/GitHub visitors to explore the live API without being able to trigger expensive operations.

#### Cost controls

Configure conservative operational safeguards:

- Cloud Run scale-to-zero,
- low maximum instance count,
- billing/budget alerts,
- resource limits,
- no automatic paid scaling as an MVP objective.

#### CI/CD relationship

The current GitHub Actions pipeline remains CI-only.

Deployment automation is not required immediately.

A later implementation step may add an explicit deployment job once the application containerization and deployment configuration are stable.

#### Alternative cloud providers

Azure Container Apps and AWS remain valid alternatives, but are not selected for the MVP.

The chosen deployment target is Google Cloud Run because it provides a simple container-based, scale-to-zero model that fits the current architecture and portfolio workload.

**Decision summary:** Publicly deploy FastAPI on Google Cloud Run and use MongoDB Atlas Free, with scale-to-zero, conservative resource limits, public read-only endpoints, API-key-protected write/sync endpoints, and billing safeguards to target zero operating cost.

---

### Q-021 — Future AI extension

**Status:** DECIDED

**Decision:** After the core MVP is complete, add semantic search over GitHub issues and pull requests as the first AI extension.

The AI extension must remain outside the core MVP until the Python + MongoDB backend is complete and portfolio-ready.

#### Phase 1 — Semantic search

Add semantic search over issue and pull request content.

High-level flow:

```text
User query
    |
    v
EmbeddingService
    |
    v
MongoDB Vector Search
    |
    v
Relevant issues / pull requests
```

The search should use embeddings and semantic similarity rather than relying only on keyword matching.

#### Embedding abstraction

Introduce an application-level abstraction such as:

```python
class EmbeddingService(Protocol):
    async def embed(self, text: str) -> list[float]:
        ...
```

This keeps the application independent from one concrete embedding provider.

Possible implementations may later use:

- a hosted embedding model,
- Google Cloud / Vertex AI,
- another external model provider,
- a locally hosted embedding model.

The concrete provider is intentionally not fixed at this design stage.

#### MongoDB Vector Search

Store and query embeddings through MongoDB Vector Search.

The vector search layer should support repository-scoped semantic retrieval and may later combine vector similarity with metadata filters such as:

- repository,
- state,
- date range,
- resource type.

#### Data-model evolution

Extend stored GitHub content only where required by the AI use case.

For example, issue and pull request text/body may need to be stored even though the analytics MVP does not require it.

This is an intentional schema evolution driven by a new use case rather than speculative data collection.

#### Phase 2 — RAG

After semantic retrieval is working, optionally add a retrieval-augmented generation endpoint.

High-level flow:

```text
Question
   |
   v
Embedding
   |
   v
MongoDB Vector Search
   |
   v
Relevant issues / PRs
   |
   v
Context construction
   |
   v
LLM
   |
   v
Answer with explicit source references
```

The RAG layer should answer repository-engineering questions using retrieved GitHub content and should preserve source attribution.

#### Framework policy

Do not introduce LangChain or another orchestration framework in the first AI implementation.

Implement the following boundaries explicitly:

- embedding generation,
- vector retrieval,
- context construction,
- prompt construction,
- LLM client,
- source attribution.

An orchestration framework may be evaluated later if it solves a concrete problem.

#### Portfolio rationale

This extension creates a clear progression:

```text
Python + MongoDB backend
        ↓
GitHub engineering analytics
        ↓
MongoDB aggregation
        ↓
Vector Search
        ↓
Semantic Search
        ↓
RAG
```

This strengthens the project's AI-engineering value without weakening its original senior-backend focus.

**Decision summary:** The first post-MVP AI feature will be semantic search over issues and pull requests using an application-level `EmbeddingService` and MongoDB Vector Search. A RAG layer may be added later on top of the same retrieval architecture. LangChain is deferred.

---

## 8. Proposed MVP

The exact MVP will be finalized after Q-001.

Provisional MVP:

1. Register a public GitHub repository.
2. Fetch repository metadata.
3. Fetch a limited history of:
   - pull requests,
   - reviews,
   - issues,
   - commits.
4. Persist the data in MongoDB.
5. Support incremental synchronization.
6. Expose repository synchronization state.
7. Compute several engineering metrics using MongoDB aggregation pipelines.
8. Expose metrics through REST endpoints.
9. Include automated tests.
10. Run locally through a documented setup.

Potential API shape:

```text
POST   /repositories
GET    /repositories
GET    /repositories/{id}
POST   /repositories/{id}/sync
GET    /repositories/{id}/sync-status

GET    /repositories/{id}/analytics/activity
GET    /repositories/{id}/analytics/pull-requests
GET    /repositories/{id}/analytics/issues
GET    /repositories/{id}/analytics/contributors
```

This API is provisional.

---

## 9. Implementation Roadmap

Legend:

- ✅ Done
- 🟡 In progress
- ⬜ Not started
- ⏸ Deferred

### Phase 0 — Project Definition

- ✅ Select project topic
- ✅ Define portfolio objective
- ✅ Select Python + MongoDB as primary technologies
- ✅ Decide to use public GitHub repositories as real input data
- ✅ Decide that arbitrary repositories should eventually be supported
- ✅ Choose repository name
- ✅ Write repository description
- ✅ Define analytics requirements
- 🟡 Define MVP scope
- ⬜ Select initial sample repositories

---

### Phase 1 — Architecture and Data Model

- ✅ Select GitHub REST API for the MVP
- ✅ Select FastAPI as Python framework
- ✅ Select direct PyMongo usage
- ✅ Define domain model
- ✅ Define MongoDB collections
- ✅ Decide embedding vs. referencing
- ✅ Define initial indexes
- ✅ Define synchronous MVP synchronization architecture
- 🟡 Define error handling strategy
- ✅ Define idempotency strategy
- ✅ Define configuration model
- ⬜ Create architecture documentation

Deliverable:

```text
docs/architecture.md
```

---

### Phase 2 — Project Skeleton

- ⬜ Initialize Python project with isolated environment
- ⬜ Add `uv` project/dependency management
- ⬜ Add FastAPI
- ⬜ Add MongoDB connection
- ⬜ Add `pydantic-settings` configuration
- ⬜ Add structured logging and correlation IDs
- ⬜ Add `/health` endpoint
- ⬜ Add test infrastructure
- ⬜ Add Ruff lint/format and mypy type checking
- ⬜ Add Docker Compose for MongoDB development instance
- ⬜ Add `.env.example` and `.gitignore` secret rules

---

### Phase 3 — GitHub API Client

- ⬜ Implement authentication
- ⬜ Implement repository metadata retrieval
- ⬜ Implement GitHub Link-header pagination
- ⬜ Implement pull request retrieval
- ⬜ Implement review retrieval
- ⬜ Implement issue retrieval
- ⬜ Implement commit retrieval
- ⬜ Handle API errors
- ⬜ Handle GitHub rate limits and reset semantics
- ⬜ Implement bounded retry/backoff
- ⬜ Add GitHub API client tests

---

### Phase 4 — Persistence

- ⬜ Implement repository persistence
- ⬜ Implement pull request persistence
- ⬜ Implement embedded review persistence in pull requests
- ⬜ Implement embedded commit persistence in pull requests
- ⬜ Implement issue persistence
- ⬜ Implement indexes
- ⬜ Implement idempotent upserts
- ⬜ Add MongoDB schema validation where useful
- ⬜ Add persistence integration tests

---

### Phase 5 — Synchronization

- ⬜ Implement initial import
- ⬜ Persist synchronization state
- ⬜ Implement checkpoint-based incremental import
- ⬜ Handle interrupted synchronization with safe replay
- ⬜ Handle partial failures
- ⬜ Add synchronization status endpoint
- ⬜ Add sync metrics/logging
- ⬜ Test restartability and idempotency

---

### Phase 6 — Analytics

Confirmed MVP analytics:

- ⬜ Pull request lead time
- ⬜ Time to first review
- ⬜ Pull request size statistics
- ⬜ Pull request size vs. review time
- ⬜ Contributor activity
- ⬜ Issue resolution time
- ⬜ Repository activity trends over time for pull requests and issues
- ⬜ MongoDB aggregation pipelines
- ⬜ Analytics API endpoints
- ⬜ Analytics tests

Deferred analytics may include:

- Issue backlog evolution
- Pull request merge-rate dashboards
- Release analytics
- Contributor concentration
- Bus-factor-like indicators

---

### Phase 7 — Performance and Senior-Level Engineering Concerns

- ⬜ Analyze MongoDB query plans
- ⬜ Verify index usage
- ⬜ Test larger datasets
- ⬜ Measure ingestion performance
- ⬜ Measure analytics query performance
- ⬜ Eliminate N+1-style access patterns
- ⬜ Document consistency decisions
- ⬜ Document embedding/reference trade-offs
- ⬜ Document failure scenarios
- ⬜ Document scalability constraints

Potential deliverable:

```text
docs/performance.md
```

---

### Phase 8 — CI and Project Quality

- ⬜ Create GitHub Actions quality/test workflow
- ⬜ Run Ruff linting and formatting checks in CI
- ⬜ Run mypy type checking in CI
- ⬜ Run unit tests in CI
- ⬜ Run MongoDB integration tests in CI
- ⬜ Add CI coverage report
- ⬜ Add pre-commit configuration for Ruff and mypy

---

### Phase 9 — Documentation and Portfolio Presentation

- ⬜ Write professional `README.md`
- ⬜ Add architecture diagram
- ⬜ Explain why MongoDB was selected
- ⬜ Explain data model decisions
- ⬜ Add example API calls
- ⬜ Add example analytics output
- ⬜ Add local and public deployment setup instructions
- ⬜ Add sample screenshots if useful
- ⬜ Document known limitations
- ⬜ Add future roadmap
- ⬜ Prepare LinkedIn project description

README should explicitly answer:

> Why MongoDB instead of a relational database?

and:

> Which engineering problems does this project solve beyond CRUD?

---

### Phase 10 — Optional Advanced Features

- ⏸ Scheduled synchronization
- ⏸ Multiple worker processes
- ⏸ Caching
- ⏸ Prometheus metrics
- ⏸ Grafana dashboard
- ⏸ OpenTelemetry
- ⏸ Implement Google Cloud Run + MongoDB Atlas deployment
- ⏸ Authentication / authorization
- ⏸ AI / semantic search extension

---

## 10. Expected Senior Backend Engineering Topics

The project should provide concrete examples for discussing the following topics in an interview.

### Data modeling

- Why certain documents are embedded
- Why certain entities are referenced
- Duplication vs. query efficiency
- Mutable vs. immutable GitHub data
- Historical snapshots

### Consistency

- Idempotent writes
- Duplicate prevention
- Partial synchronization
- Eventual consistency between GitHub and the local database

### Performance

- Index selection
- Aggregation performance
- Query plans
- Pagination
- Batch writes
- API call minimization

### Resilience

- GitHub API failures
- Rate limiting
- Retries
- Backoff
- Restartable imports
- Corrupt/incomplete data handling

### API design

- Resource-oriented endpoints
- Error responses
- Pagination
- Long-running jobs
- HTTP semantics

### Maintainability

- Clear boundaries between:
  - API layer
  - service/domain layer
  - GitHub client
  - persistence layer
  - analytics layer

### Testing

- Unit tests
- HTTP client tests
- MongoDB integration tests
- API tests
- Failure-path tests

---

## 11. Potential Package Structure

Provisional only:

```text
github-engineering-analytics/
|
├── src/
│   └── github_analytics/
│       ├── api/
│       ├── config/
│       ├── domain/
│       ├── github/
│       ├── persistence/
│       ├── services/
│       ├── analytics/
│       └── main.py
|
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
|
├── docs/
│   ├── architecture.md
│   └── performance.md
|
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── README.md
└── PROJECT.md
```

This structure is not yet a confirmed decision.

---

## 12. Non-Goals for the Initial Version

The first version should avoid unnecessary complexity.

Not required initially:

- Complex frontend
- Kubernetes
- Multiple microservices
- Kafka
- Full event-driven architecture
- Enterprise authentication
- Massive GitHub-wide ingestion
- Real-time processing
- AI integration
- Premature cloud deployment

These can be added only when they solve a real problem or materially improve the portfolio value.

---

## 13. Development Principles

1. Prefer a small but production-quality system over a large unfinished system.
2. Every major technology should solve a real problem.
3. MongoDB-specific design decisions must be explainable.
4. Avoid tutorial-style architecture.
5. Favor explicit code over unnecessary framework magic.
6. Treat failure paths as first-class use cases.
7. Tests should validate behavior, not implementation details.
8. Keep domain logic independent from HTTP and persistence where practical.
9. Optimize only after measuring, but design with realistic scale in mind.
10. Document important trade-offs as they are made.

---

## 14. Project Continuation Instructions

When continuing this project in another ChatGPT conversation:

1. Provide this `PROJECT.md` file.
2. Treat **Confirmed Decisions** as authoritative.
3. Do not reopen confirmed decisions unless there is a concrete technical reason.
4. Check **Current Project Status**.
5. Find the first unresolved item in **Open Design Questions**.
6. Check the roadmap for the current phase.
7. Continue from **Next Action** below.
8. Update this file whenever a meaningful architectural or scope decision is made.

The purpose of this document is to prevent loss of project context between conversations.

---

## 15. Next Action

### NEXT: Start implementation planning

All current architecture/design questions through Q-021 are resolved.

The next step is to turn the design into an implementation sequence.

Start with the first coding milestone:

1. initialize the Python project with `uv`,
2. create the package/module structure,
3. add FastAPI application bootstrap,
4. add typed settings with `pydantic-settings`,
5. configure Ruff, mypy, pytest, and pre-commit,
6. add Docker Compose for local MongoDB,
7. define MongoDB collections/index initialization,
8. add the first repository API and persistence slice.

Implementation should continue incrementally, preserving the architectural boundaries defined in this document.

---

## 16. Decision Log

| ID | Decision | Status |
|---|---|---|
| D-001 | Build a GitHub engineering analytics backend | ✅ Confirmed |
| D-002 | Use Python and MongoDB as primary technologies | ✅ Confirmed |
| D-003 | Use real public GitHub repositories as input | ✅ Confirmed |
| D-004 | Support arbitrary public repositories eventually | ✅ Confirmed |
| D-005 | Position the project as senior backend engineering, not CRUD | ✅ Confirmed |
| D-006 | Use seven selected engineering analytics metrics for the MVP | ✅ Confirmed |
| D-007 | Embed PR commits and avoid a separate commits collection in the MVP | ✅ Confirmed |
| D-008 | Use four top-level collections with embedded PR reviews and commits | ✅ Confirmed |
| D-009 | Use aggregation pipelines, selective indexes, bulk upserts, schema validation, and query-plan analysis | ✅ Confirmed |
| D-010 | Use FastAPI as the API framework and keep it confined to the transport layer | ✅ Confirmed |
| D-011 | Use PyMongo directly instead of an ODM | ✅ Confirmed |
| D-012 | Run bounded repository synchronization synchronously in the MVP API request | ✅ Confirmed |
| D-013 | Use resource-level updated-at checkpoints and idempotent replay-safe synchronization | ✅ Confirmed |
| D-014 | Use authenticated serial GitHub requests with bounded retry/backoff and rate-limit awareness | ✅ Confirmed |
| D-015 | Use GitHub REST API for the MVP and defer GraphQL | ✅ Confirmed |
| D-016 | No JWT/user authentication in MVP; optional API-key protection for public write/sync endpoints | ✅ Confirmed |
| D-017 | Use pydantic-settings with environment variables, local .env, and committed .env.example | ✅ Confirmed |
| D-018 | Use layered testing with Testcontainers-based real MongoDB integration tests and mocked GitHub HTTP transport | ✅ Confirmed |
| D-019 | Run FastAPI on the host, MongoDB in Docker Compose, and integration-test MongoDB via Testcontainers | ✅ Confirmed |
| D-020 | Use uv with pyproject.toml, committed uv.lock, local .venv, and separate runtime/dev dependencies | ✅ Confirmed |
| D-021 | Use Ruff for lint/format, mypy for typing, pytest for tests, and pre-commit for local quality checks | ✅ Confirmed |
| D-022 | Use GitHub Actions with parallel quality and test jobs; defer image build/deployment | ✅ Confirmed |
| D-023 | Use structured logging, correlation IDs, health/readiness checks, and centralized exception handling | ✅ Confirmed |
| D-024 | Keep the MVP backend/API-only and use FastAPI generated API documentation as the UI | ✅ Confirmed |
| D-025 | Deploy publicly on Google Cloud Run with MongoDB Atlas Free and conservative free-tier cost controls | ✅ Confirmed |
| D-026 | Add post-MVP semantic search with EmbeddingService and MongoDB Vector Search; defer RAG orchestration frameworks | ✅ Confirmed |

---

## 17. Progress Log

### 2026-09-06

- Project topic selected.
- GitHub Analytics chosen over event analytics and IoT telemetry.
- Real public GitHub repositories selected as the primary data source.
- Decided that the architecture should eventually support arbitrary repositories.
- Repository name selected: `github-engineering-analytics`.
- Repository description defined.
- `PROJECT.md` created as the project's persistent planning and status document.
- Next task identified: define MVP analytics questions before designing the MongoDB schema.

### 2026-09-07

- Q-001 resolved.
- MVP analytics scope fixed at seven metrics:
  - pull request lead time,
  - time to first review,
  - pull request size statistics,
  - pull request size vs. review time,
  - contributor activity,
  - issue resolution time,
  - repository activity trends over time.
- Additional analytics explicitly deferred until after the MVP.
- Next task changed to Q-002: determine which GitHub entities and fields must be persisted.
- Q-002 resolved.
- Top-level MVP collections fixed as `repositories`, `pull_requests`, `issues`, and `sync_states`.
- Reviews will be embedded in pull request documents.
- Pull-request commits will be embedded in pull request documents.
- A separate `commits` collection will not be created for the MVP.
- Repository-wide commit activity was removed from the MVP analytics scope.
- Next task changed to Q-003: design the detailed MongoDB document schema.
- Q-003 resolved.
- Detailed MongoDB document schema defined.
- `reviews[]` and `commits[]` confirmed as embedded pull request data.
- Initial repository-scoped unique and compound indexes defined.
- Derived analytics values will be calculated at query time rather than persisted.
- Multikey index limitations for the two embedded arrays documented as an accepted trade-off.
- Next task changed to Q-004: select MongoDB features to demonstrate intentionally.
- Q-004 resolved.
- Aggregation pipelines selected as the primary analytics mechanism.
- `$unwind`, `$facet`, date operators, compound indexes, selective multikey indexes, bulk upserts, schema validation, and `explain()` were included in the MVP technology scope.
- `$lookup`, change streams, TTL indexes, text search, time-series collections, and window functions were deferred unless justified by a future requirement.
- Next task changed to Q-005: select the Python web framework.

---

### 2026-09-17

- Q-005 resolved: FastAPI selected as the HTTP API framework.
- FastAPI is explicitly limited to the API/transport layer.
- Q-006 resolved: direct PyMongo usage selected instead of an ODM.
- The async PyMongo API is preferred so database access fits the asynchronous backend model.
- Q-007 resolved: repository synchronization will run synchronously inside the API request for the MVP.
- Synchronization volume will be bounded by configurable limits.
- Only one synchronization may run per repository at a time.
- Synchronization logic will remain in an application service so it can later be moved to a background worker without redesigning the core logic.
- Next task changed to Q-008: define incremental synchronization and checkpoint semantics.

---

### 2026-09-19

- Q-008 resolved: incremental synchronization uses independent resource-level update-time checkpoints.
- Checkpoints advance only after successful resource synchronization.
- Sync writes are idempotent upserts; interrupted runs safely replay from the previous checkpoint.
- Updated pull requests trigger refresh of embedded `reviews[]` and `commits[]`.
- Q-009 resolved: GitHub API access will be authenticated and serial in the MVP.
- Rate-limit headers are monitored; bounded exponential backoff and finite retry budgets are used.
- Conditional requests may be used where they provide concrete benefit.
- Q-010 resolved: GitHub REST API selected for the MVP.
- GraphQL deferred as a later comparison/optimization exercise.
- Next task changed to Q-011: decide authentication for the application's own API.

### 2026-09-23

- Q-011 resolved: no user/JWT authentication in the MVP.
- Local development may run without authentication.
- Public deployments will protect write/synchronization endpoints with a simple API key if needed.
- Q-012 resolved: `pydantic-settings` selected for centralized typed configuration.
- Environment variables are the canonical configuration source.
- Local `.env` files are allowed but excluded from version control.
- `.env.example` will document supported configuration values without secrets.
- GitHub tokens, API keys, and credential-bearing MongoDB URIs are treated as secrets.
- Next task changed to Q-013: define the testing strategy.


### 2026-10-21

- Q-013 resolved: layered testing strategy selected.
- Unit tests will cover application/service logic without real external systems.
- GitHub client tests will mock the HTTP transport rather than call GitHub.
- MongoDB integration tests will use a real MongoDB instance through Testcontainers.
- FastAPI endpoint tests and explicit failure-path tests are required.
- Only a small number of end-to-end smoke tests are planned for the MVP.
- Approximately 80% overall code coverage is a guideline, not a hard target.
- Next task changed to Q-014: define the local development environment.

---

### 2026-10-29

- Q-014 resolved: local development environment defined.
- FastAPI will run directly on the developer host inside an isolated Python environment.
- MongoDB will run through Docker Compose with a persistent development volume.
- Integration tests will use a separate Testcontainers-managed MongoDB instance.
- Mongo Express is optional and not part of the default stack.
- Containerizing the FastAPI application itself is deferred until the application is sufficiently stable.
- Next task changed to Q-015: select packaging and dependency management.

---

### 2026-10-29 — Packaging decision

- Q-015 resolved: `uv` selected for Python project and dependency management.
- Dependencies will be declared in `pyproject.toml`.
- `uv.lock` will be committed for reproducible environments.
- `.venv/` remains local and uncommitted.
- Runtime and development dependencies will be managed separately.
- Poetry and pip/requirements-based workflows are not used in the MVP.
- Next task changed to Q-016: select code-quality tooling.

---

### 2026-10-29 — Code quality decision

- Q-016 resolved: code-quality tooling selected.
- Ruff will handle both linting and formatting.
- Black will not be used separately.
- mypy will provide static type checking with a strict posture for project-owned code.
- pytest remains the main test runner.
- pre-commit will run fast local checks such as Ruff and mypy.
- Full unit, API, GitHub-client, integration, and coverage checks remain CI responsibilities.
- Next task changed to Q-017: define CI/CD.

---

### 2026-10-29 — CI, observability, and UI decisions

- Q-017 resolved: GitHub Actions selected for CI.
- CI will run parallel `quality` and `test` jobs on pull requests and pushes to `main`.
- Quality checks include Ruff linting, Ruff formatting validation, and mypy.
- The test job runs the complete pytest suite, Testcontainers integration tests, and coverage reporting.
- Docker image building and deployment remain outside the MVP CI pipeline.
- Q-018 resolved: MVP observability defined.
- Structured logging, request/correlation IDs, synchronization lifecycle events, `/health`, `/ready`, and centralized exception handling are included.
- Prometheus, Grafana, OpenTelemetry, and a dedicated metrics endpoint are deferred.
- Q-019 resolved: the MVP remains backend/API-only.
- FastAPI Swagger/OpenAPI documentation will be the primary interactive interface.
- A standalone frontend/dashboard is deferred.
- Next task changed to Q-020: decide the deployment target.

---

### 2026-10-29 — Deployment decision

- Q-020 resolved: public deployment target selected.
- FastAPI will be deployed on Google Cloud Run.
- MongoDB will use a MongoDB Atlas Free cluster, preferably backed by GCP.
- Cloud Run will use scale-to-zero and a low maximum instance count to minimize cost risk.
- Read-only analytics and generated API documentation may remain public.
- Write and synchronization endpoints remain protected with an API key.
- Billing alerts and conservative resource limits are required.
- The deployment is designed to remain within commercial cloud free tiers and target 0 EUR operating cost.
- Deployment automation remains deferred until application containerization and deployment configuration are stable.
- Next task changed to Q-021: decide the future AI extension.

---

### 2026-10-29 — AI extension decision

- Q-021 resolved: the first post-MVP AI feature will be semantic search over issues and pull requests.
- Embedding generation will be isolated behind an application-level `EmbeddingService`.
- MongoDB Vector Search will provide semantic retrieval.
- Issue/PR text will be stored only when the AI use case requires it.
- A later RAG layer may answer repository-engineering questions using retrieved GitHub sources.
- Source attribution is required for RAG answers.
- LangChain and similar orchestration frameworks are deferred for the first AI implementation.
- All current design questions through Q-021 are now resolved.
- Next task changed from architecture decisions to implementation planning.

---

## 18. Project Completion Definition

The project can be considered portfolio-ready when:

- A user can configure/register at least one public GitHub repository.
- Data can be imported reliably.
- A repeated synchronization does not create duplicates.
- Incremental synchronization works.
- MongoDB usage is justified and documented.
- Several non-trivial engineering metrics are computed using MongoDB.
- REST endpoints expose the results.
- Important queries have appropriate indexes.
- Automated tests cover core behavior and failure paths.
- CI runs automatically on GitHub.
- Docker-based local startup is documented.
- README explains architecture, design decisions, trade-offs, and usage.
- The codebase is clean enough to be reviewed during a technical interview.
