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

**Next step:** Select the Python web framework for the API layer.

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
   Weekly/monthly trends for commits, pull requests, and issues.

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

**Status:** OPEN

Primary candidate:

- FastAPI

Alternatives:

- Flask
- Django / Django REST Framework

Likely direction: FastAPI because the project is API-centric and should demonstrate modern Python typing and asynchronous I/O.

**Decision:** _To be confirmed._

---

### Q-006 — Which MongoDB Python driver / abstraction layer should be used?

**Status:** OPEN

Candidates:

- PyMongo
- PyMongo Async API
- ODMantic
- Beanie
- MongoEngine

Key decision:

Should the project demonstrate MongoDB directly through the official driver, or use an ODM?

Possible preference for portfolio value: retain enough direct MongoDB interaction that document modeling, indexes, and aggregation pipelines remain visible.

**Decision:** _To be determined._

---

### Q-007 — Sync architecture: synchronous request, background job, or both?

**Status:** OPEN

Potential model:

```text
POST /repositories
        |
        v
Register repository
        |
        v
Background synchronization job
        |
        v
GitHub API -> MongoDB
```

Questions:

- Should imports happen asynchronously?
- Should an API request start an import and return a job ID?
- Do we need a job/status collection?
- What scheduler should later run incremental updates?

**Decision:** _To be determined._

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

**Status:** OPEN

Possible MVP choices:

- No authentication for local/demo use
- API key
- JWT authentication

Authentication should only be added if it demonstrates useful backend engineering without distracting from the main project goals.

**Decision:** _To be determined._

---

### Q-012 — Configuration and secrets

**Status:** OPEN

Expected configuration:

- MongoDB URI
- GitHub token
- Database name
- Import limits
- Logging level

Likely mechanisms:

- Environment variables
- `.env` for local development
- `.env.example` committed to Git
- Secrets excluded from Git

**Decision:** _To be confirmed._

---

### Q-013 — Testing strategy

**Status:** OPEN

Candidates:

- Unit tests
- Repository/data-access tests
- Integration tests against MongoDB
- API tests
- GitHub API client tests using mocked HTTP responses
- End-to-end tests
- Testcontainers

Questions:

- Use Docker MongoDB for integration tests?
- Use Testcontainers?
- What coverage target is meaningful?

**Decision:** _To be determined._

---

### Q-014 — Local development environment

**Status:** OPEN

Likely setup:

- Python virtual environment
- Docker Compose
- MongoDB container
- Application container later
- Optional Mongo Express or another database UI

**Decision:** _To be determined._

---

### Q-015 — Packaging and dependency management

**Status:** OPEN

Candidates:

- `uv`
- Poetry
- pip + requirements files

**Decision:** _To be determined._

---

### Q-016 — Code quality tooling

**Status:** OPEN

Candidates:

- Ruff
- Black
- mypy
- pytest
- pre-commit

**Decision:** _To be determined._

---

### Q-017 — CI/CD

**Status:** OPEN

Likely CI platform:

- GitHub Actions

Possible pipeline:

```text
Push / Pull Request
        |
        +--> lint
        +--> type checking
        +--> unit tests
        +--> integration tests
        +--> build Docker image
```

Deployment is optional for the first version.

**Decision:** _To be determined._

---

### Q-018 — Observability

**Status:** OPEN

Possible scope:

- Structured logging
- Request IDs / correlation IDs
- Import statistics
- Sync duration
- GitHub API request counts
- Errors and retries
- Health endpoint
- Readiness endpoint
- Metrics endpoint

Optional later:

- Prometheus
- Grafana
- OpenTelemetry

**Decision:** _To be determined._

---

### Q-019 — Should the application have a UI?

**Status:** OPEN

Options:

- Backend/API only
- Swagger/OpenAPI UI only
- Small dashboard
- Separate frontend

Initial preference: backend-first. A frontend should only be added if it materially improves the portfolio demonstration.

**Decision:** _To be determined._

---

### Q-020 — Deployment target

**Status:** OPEN

Possibilities:

- Local Docker only
- AWS
- Azure
- Render
- Railway
- Fly.io
- Other

Deployment is not required for the initial coding phase.

**Decision:** _To be determined later._

---

### Q-021 — Future AI extension

**Status:** OPEN / FUTURE

Potential extensions:

- Semantic issue search
- Semantic pull request search
- Issue classification
- PR summarization
- Repository knowledge assistant
- Embeddings
- RAG over repository engineering activity
- Natural-language analytics

This is explicitly a future extension and should not complicate the MVP.

**Decision:** _Deferred._

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
- ⬜ Select Python framework
- ⬜ Select MongoDB driver / ODM
- ✅ Define domain model
- ✅ Define MongoDB collections
- ✅ Decide embedding vs. referencing
- ✅ Define initial indexes
- ⬜ Define synchronization architecture
- ⬜ Define error handling strategy
- ✅ Define idempotency strategy
- ⬜ Define configuration model
- ⬜ Create architecture documentation

Deliverable:

```text
docs/architecture.md
```

---

### Phase 2 — Project Skeleton

- ⬜ Initialize Python project
- ⬜ Add dependency management
- ⬜ Add FastAPI or selected framework
- ⬜ Add MongoDB connection
- ⬜ Add application configuration
- ⬜ Add structured logging
- ⬜ Add health endpoint
- ⬜ Add test infrastructure
- ⬜ Add linting/type checking
- ⬜ Add Docker Compose for MongoDB
- ⬜ Add `.env.example`

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

- ⬜ Create GitHub Actions workflow
- ⬜ Run linting in CI
- ⬜ Run type checking in CI
- ⬜ Run unit tests in CI
- ⬜ Run MongoDB integration tests in CI
- ⬜ Add coverage report
- ⬜ Add pre-commit configuration

---

### Phase 9 — Documentation and Portfolio Presentation

- ⬜ Write professional `README.md`
- ⬜ Add architecture diagram
- ⬜ Explain why MongoDB was selected
- ⬜ Explain data model decisions
- ⬜ Add example API calls
- ⬜ Add example analytics output
- ⬜ Add local setup instructions
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
- ⏸ Cloud deployment
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

### NEXT: Decide application API authentication

Resolve **Q-011**:

> Does the application's own FastAPI API need authentication in the MVP?

Possible choices:

- no authentication for local/demo use,
- simple API key,
- JWT-based authentication.

The decision should consider:

- portfolio value,
- implementation complexity,
- whether authentication contributes to the core learning goals,
- whether the application will be deployed publicly,
- whether protecting GitHub synchronization endpoints is necessary in the MVP.

Authentication should only be included if it adds meaningful backend engineering value without distracting from the Python + MongoDB focus.

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
| D-013 | Use resource-level updated-at checkpoints and idempotent replay-safe synchronization | ✅ Confirmed |
| D-014 | Use authenticated serial GitHub requests with bounded retry/backoff and rate-limit awareness | ✅ Confirmed |
| D-015 | Use GitHub REST API for the MVP and defer GraphQL | ✅ Confirmed |

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
