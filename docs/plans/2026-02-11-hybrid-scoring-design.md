# Hybrid Scoring for Programme Recommendations

**Date**: 2026-02-11
**Status**: Approved

## Problem

The current recommendation system compares user profile text embeddings against scraped programme document chunks via cosine similarity. Because these are fundamentally different text domains (applicant self-descriptions vs programme marketing content), scores naturally cap at ~50% even for perfect matches.

The spider chart profile scores (hard-coded per programme) are only used for visualization, not scoring.

## Solution: Hybrid Scoring

Combine **direct spider chart comparison** with **semantic embedding similarity** using adaptive weights.

### Formula

```
final_score = w_profile * profile_sim + w_semantic * semantic_sim
```

**Adaptive Weights**:
- With CV text: `w_profile=0.4, w_semantic=0.6`
- Without CV text: `w_profile=0.8, w_semantic=0.2`

### Profile Similarity (Normalized Euclidean Distance)

```
max_distance = sqrt(7 * (5-1)^2) = sqrt(112) ~ 10.58
actual_distance = sqrt(sum((user_i - prog_i)^2))
profile_sim = 1 - (actual_distance / max_distance)
```

Score all 22 programmes, not just those from vector search.

### Semantic Similarity (Fixed-Range Rescale)

```
rescaled = (raw_cosine_sim - 0.25) / (0.60 - 0.25)
semantic_sim = clamp(rescaled, 0.0, 1.0)
```

Maps the observed 0.25-0.60 raw range to 0.0-1.0.

Programmes without vector search hits get `semantic_sim = 0`.

## Changes

**Only file**: `backend/app/api/routes/recommend.py`

1. Add `_profile_similarity()` helper
2. Add `_rescale_semantic()` helper
3. Rewrite `/match` endpoint scoring logic

No frontend, database, or ingestion changes needed.
