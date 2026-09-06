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

**Next step:** Decide which GitHub entities must be stored to support the selected MVP analytics.

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
- Repository activity trends over time

**Reasoning:**  
This set is broad enough to demonstrate meaningful MongoDB aggregation, time-based analysis, relationships between GitHub entities, indexing, and senior backend design without turning the project into a large analytics product.

Additional metrics are deferred until after the MVP.

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

**Status:** OPEN

Candidates:

- Repository
- Commit
- Pull request
- Pull request review
- Issue
- Contributor
- User
- Label
- Release
- Branch

Questions to answer:

- Which objects belong in separate collections?
- Which objects should be embedded?
- Which GitHub data should not be persisted at all?

**Decision:** _To be determined after Q-001._

---

### Q-003 — What should the MongoDB document model look like?

**Status:** OPEN

Topics:

- Embedded vs. referenced documents
- Collection boundaries
- Denormalization strategy
- Snapshot data vs. normalized identity data
- Historical values
- Update frequency
- Document growth
- MongoDB document size constraints

**Decision:** _To be determined after analytics requirements are known._

---

### Q-004 — Which MongoDB features should the project intentionally demonstrate?

**Status:** OPEN

Candidates:

- Compound indexes
- Multikey indexes
- TTL indexes
- Aggregation pipelines
- `$lookup`
- `$group`
- `$facet`
- Window functions
- Text search
- Schema validation
- Change streams
- Time-series collections

Important principle:

Features should only be added when they fit the use case. The project should not artificially use MongoDB features merely to increase the technology list.

**Decision:** _To be determined._

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

**Status:** OPEN

Topics:

- Last successful synchronization timestamp
- GitHub `updated_at`
- Pagination state
- Duplicate prevention
- Idempotent upserts
- Partial failures
- Retry policy
- Restartability
- Sync checkpoints

**Decision:** _To be determined._

---

### Q-009 — How should GitHub API rate limiting be handled?

**Status:** OPEN

Topics:

- Authenticated vs. unauthenticated requests
- Rate-limit headers
- Backoff
- Retry
- Request throttling
- API caching
- Incremental sync optimization

**Decision:** _To be determined._

---

### Q-010 — GitHub REST API or GraphQL API?

**Status:** OPEN

Options:

- GitHub REST API
- GitHub GraphQL API
- Hybrid

Factors:

- Implementation complexity
- Request count
- Nested data retrieval
- Pagination
- Rate limits
- Portfolio value

**Decision:** _To be determined._

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

- ⬜ Select GitHub REST / GraphQL strategy
- ⬜ Select Python framework
- ⬜ Select MongoDB driver / ODM
- ⬜ Define domain model
- ⬜ Define MongoDB collections
- ⬜ Decide embedding vs. referencing
- ⬜ Define indexes
- ⬜ Define synchronization architecture
- ⬜ Define error handling strategy
- ⬜ Define idempotency strategy
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
- ⬜ Implement pagination
- ⬜ Implement pull request retrieval
- ⬜ Implement review retrieval
- ⬜ Implement issue retrieval
- ⬜ Implement commit retrieval
- ⬜ Handle API errors
- ⬜ Handle rate limits
- ⬜ Implement retry/backoff
- ⬜ Add GitHub API client tests

---

### Phase 4 — Persistence

- ⬜ Implement repository persistence
- ⬜ Implement pull request persistence
- ⬜ Implement review persistence
- ⬜ Implement issue persistence
- ⬜ Implement commit persistence
- ⬜ Implement indexes
- ⬜ Implement idempotent upserts
- ⬜ Add MongoDB schema validation where useful
- ⬜ Add persistence integration tests

---

### Phase 5 — Synchronization

- ⬜ Implement initial import
- ⬜ Persist synchronization state
- ⬜ Implement incremental import
- ⬜ Handle interrupted synchronization
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
- ⬜ Repository activity trends over time
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

### NEXT: Define the required GitHub entities

Resolve **Q-002**:

> Which GitHub entities must be stored to support the selected MVP analytics?

The chosen analytics are now fixed, so the next task is to determine the minimum useful persisted dataset.

This decision should answer:

- Which GitHub entities are required
- Which entities should have their own MongoDB collection
- Which data should be embedded
- Which GitHub fields are actually needed
- Which data can be fetched but not persisted
- Which relationships must be preserved for analytics

Do **not** finalize the MongoDB schema before this entity-level scope is sufficiently resolved.

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
