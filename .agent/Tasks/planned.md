# Planned Tasks

**Last Updated**: 2026-03-28

---

## 6. Deploy Admin Dashboard to whitepine-tech.com (Hetzner)
**Priority**: MEDIUM
**Estimated**: 1-2 hours
**Dependencies**: Working admin panel locally

**Goal**: Deploy the Flask admin dashboard to the WhitePineTech Hetzner server so it's accessible via whitepine-tech.com.

**Requirements**:
- [ ] Run behind nginx reverse proxy (e.g., `news.whitepine-tech.com` or `/news-admin`)
- [ ] Systemd service for auto-start on reboot
- [ ] Environment variables / secrets secured on server
- [ ] Auth/login enabled (already exists in admin panel)
- [ ] SSL via Let's Encrypt

**Technical Notes**:
- Server: 5.78.128.255 (whitepine/whitepine-root SSH alias)
- Admin panel is a Flask app in `admin-panel/`
- Review `deploy_to_hetzner.sh` — may already have deployment scaffolding

---

## 2. Find Better AI Feed
**Priority**: MEDIUM
**Estimated**: 30 minutes
**Dependencies**: None

**Goal**: Replace The Verge AI with a more practical, how-to focused AI source

**Candidate Sources to Evaluate**:
- **Practical/How-To Focus**:
  - Simon Willison's Weblog (https://simonwillison.net/atom/everything/) - AI tools, prompts, practical tutorials
  - Towards Data Science RSS - hands-on ML/AI tutorials
  - Machine Learning Mastery - practical guides

- **Industry News + Tutorials Mix**:
  - Import AI Newsletter RSS - weekly AI roundup
  - The Batch (deeplearning.ai) - Andrew Ng's newsletter
  - AI Weekly - curated AI news

- **Developer-Focused**:
  - Hugging Face Blog - model releases, tutorials
  - LangChain Blog - AI app development
  - OpenAI Blog - official updates + guides

**Evaluation Criteria**:
- [ ] Has working RSS feed
- [ ] Updates regularly (at least weekly)
- [ ] Includes practical how-to content
- [ ] Not just hype/news, but actionable info

**Notes**:
- Current feed (The Verge AI) is good for news but light on practical content
- Consider adding 2 AI sources: one news, one tutorials

---

## 3. Optimize After First Week
**Priority**: LOW
**Estimated**: 1 hour
**Dependencies**: 7 days of digests received

**Acceptance Criteria**:
- Review digest quality
- Adjust sources if needed
- Fine-tune keyword filters

### Subtasks
- [ ] 3.1 Review 7 days of digests
- [ ] 3.2 Note any missing topics or excessive noise
- [ ] 3.3 Adjust feeds.yaml as needed

---

## 4. Robust X/Twitter Feed Reimplementation
**Priority**: MEDIUM
**Estimated**: 1 hour
**Dependencies**: None

**Goal**: Restore trending topics with better parsing logic.

**Technical Notes**:
- Previous implementation used Serper Search which returned split tokens (e.g., "Charlie", "Kirk") and UI noise.
- Future implementation should use an API that provides full trending topics (n-grams) or a more sophisticated cleaner.
- Filter out tokens like "Explore", "more", "Trending", "X".

---

## 5. Morning Historical Context
**Priority**: HIGH
**Estimated**: 45 minutes
**Dependencies**: Wikipedia API

**Goal**: Add "On This Day" section to morning emails.

**Requirements**:
- Fetch events from Wikipedia REST API.
- Filter for years 1972 or 1992.
- Display 3 events with Grokipedia links.

