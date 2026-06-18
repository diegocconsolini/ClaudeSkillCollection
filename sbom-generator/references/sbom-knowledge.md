# SBOM Knowledge Pack — grounded reference for the /sbom skill

> Sourced from a verified deep-research pass (2026-06-18). Claims marked ✓ were
> independently verified (≥2/3 adversarial vote); claims marked ⚠ are
> research-reported but not first-party-confirmed — verify before relying on them.
> Full plan: `docs/plans/2026-06-18-audit-supplychain-sbom-plan.md`.

## 1. Formats — emit BOTH

- ✓ **CycloneDX** and **SPDX** are the two NTIA- and CISA-endorsed formats. Emit
  both; downstream consumers differ. (NTIA also listed SWID; CISA's 2025 draft drops it.)
- ✓ **CycloneDX**: current spec is **v1.7** (ECMA-424, Oct 2025); **1.6 is fine** and
  is what the vendored generator emits. Mandatory top-level JSON fields: `bomFormat`
  (constant `"CycloneDX"`), `specVersion`.
- ✓ **SPDX**: **3.0.1 is finalized** (Dec 2024) but introduces breaking JSON-LD
  changes and drops Tag/Value, YAML, RDF/XML. **Default to SPDX 2.3** for consumer
  compatibility; offer 3.0 only as an explicit opt-in. The vendored generator emits 2.3.

## 2. Minimum elements

- ✓ **NTIA 7 per-component fields** (the binding baseline): Supplier, Component Name,
  Version, Other Unique Identifiers (purl/CPE), Dependency Relationship, Author of SBOM
  Data, Timestamp.
- ✓ **CISA 2025** (DRAFT, not binding as of mid-2026): renames Depth→**Coverage**
  (all transitive deps, no minimum depth) and formalizes **Known Unknowns** (an
  incomplete SBOM must say so). Treat as forward-looking best practice.
- ❌ Do NOT encode a "CISA-2025 11 mandatory fields" list — that specific enumeration
  was **refuted** in research.

## 3. Regulatory (verified)

- ✓ **US:** OMB **M-26-05 (2026-01-23)** rescinded M-22-18 and M-23-16. SBOMs are now
  an **optional, on-request** contractual term — **not** a government-wide mandate.
  (❌ Refuted: "M-26-05 points agencies to CISA-2025" — do not claim this linkage.)
- ✓ **EU CRA** (Reg. (EU) 2024/2847): in force 2024-12-10. Reporting obligations from
  **2026-09-11**; main obligations from **2027-12-11**. Manufacturers must produce/maintain
  an SBOM (Annex I). Exact format/depth wording is an open item — verify in the regulation.

## 4. Per-stack generation — ephemeral runners (add NOTHING to the target manifest)

| Stack | Lockfile/input | Canonical tool (ephemeral) |
|---|---|---|
| **npm** | `package-lock.json` v2/v3 | **vendored `generate-sbom.mjs`** (zero-dep, reads lockfile) — or `npx -y @cyclonedx/cyclonedx-npm` |
| **pnpm** | `pnpm-lock.yaml` | `npx -y @cyclonedx/cyclonedx-npm` won't read it → use **Syft** (`syft dir:.`) |
| **yarn** | `yarn.lock` | same as pnpm → **Syft** |
| **Python** | `requirements.txt`/`poetry.lock`/env | `pipx run cyclonedx-bom ...` (`cyclonedx-py`) |
| **Go** | `go.sum` | `go run github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest mod -json` |
| **Rust** | `Cargo.lock` | `cargo install --locked cargo-cyclonedx` then `cargo cyclonedx -f json` — ⚠ **caps at spec 1.5, defaults 1.3**; normalize with Syft convert if a consumer needs 1.6 |
| **Java (Maven)** | `pom.xml` | `mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom` (plugin run, not added to pom) |
| **.NET** | `.csproj` | `dotnet CycloneDX <sln> --json` (needs `dotnet restore`) |
| **polyglot** | many | `cdxgen` (20+ ecosystems) or ORT |
| **container / filesystem** | image or dir | **Syft** (`syft <image>` / `syft dir:.`) — also converts between formats |

Rule: never `npm install` (or any manifest-modifying install) to make an SBOM. Use the
vendored script for npm; ephemeral runners (`npx -y`, `pipx run`, `go run …@latest`) elsewhere.

## 5. Quality scoring + CI gate

- ✓ **sbomqs** (interlynk-io): scores 0.0–10.0 across NTIA-minimum-elements / structural /
  semantic / quality / sharing. Run ephemerally:
  `docker run --rm -v $(pwd):/app ghcr.io/interlynk-io/sbomqs:latest score /app/bom.cdx.json`
  Suggested gate: **≥ 7.0** for production, ≥ 6.0 experimental.
- ✓ **SPDX ntia-conformance-checker**: `pipx run ntia-conformance-checker` (or
  `sbomcheck --comply ntia bom.spdx.json`) to verify the NTIA-7 are present.
- Common pitfalls to surface: missing transitive deps (build- vs source-SBOM), missing
  license/hashes, no supplier, no timestamp.

## 6. Vulnerability scanning + VEX

- ✓ Feed the SBOM to **Grype**, **Trivy**, or **OSV-Scanner** (all consume CycloneDX/SPDX).
- ✓ **VEX** layers exploitability status so scanners suppress non-exploitable findings.
  **OpenVEX** is simpler than CSAF and is natively consumed by Grype/Trivy/OSV. Link a
  statement to a component by **purl** in `products[]`. Minimal OpenVEX:
  ```json
  {
    "@context": "https://openvex.dev/ns/v0.2.0",
    "@id": "https://example.com/vex-0001",
    "author": "your-org",
    "timestamp": "2026-06-18T00:00:00Z",
    "version": 1,
    "statements": [
      { "vulnerability": { "name": "CVE-2023-12345" },
        "products": [{ "@id": "pkg:npm/lodash@4.17.21" }],
        "status": "not_affected",
        "justification": "vulnerable_code_not_in_execute_path" }
    ]
  }
  ```

## 7. Signing / attestation

- ✓ **cosign v3** (Sigstore). Keyless/OIDC is the **default in CI** —
  `COSIGN_EXPERIMENTAL` is **no longer required**.
  - Container image: `cosign attest --predicate bom.cdx.json --type cyclonedx <image>@<digest>`
  - Standalone file (blob): `cosign attest-blob --predicate bom.cdx.json --type cyclonedx bom.cdx.json`
  - Verify: `cosign verify-attestation --type cyclonedx --certificate-oidc-issuer <issuer> <ref>`
- Provenance chain (who/when/from-what) complements the SBOM (what). SLSA provenance +
  in-toto attestations are the higher-assurance tier.

## 8. Supply-chain context (why this matters — 2024-2026, see incident pack)

SBOM + scan + VEX is the concrete answer to the recent npm supply-chain wave
(xz-utils CVE-2024-3094 ✓, Shai-Hulud worm Sept-2025 ✓, s1ngularity/Nx ✓,
chalk/debug crypto-clipper ✓). An SBOM lets you answer "am I shipping the compromised
version?" in seconds. Pair with: `npm ci` (lockfile integrity), `ignore-scripts`,
dependency cooldown / `min-release-age`, Trusted Publishing/OIDC + provenance.
