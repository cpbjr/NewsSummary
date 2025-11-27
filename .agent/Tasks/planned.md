# Planned Tasks

**Last Updated**: 2025-11-27

---

## 1. Configure GitHub Secrets for Email Delivery
**Priority**: HIGH
**Estimated**: 10 minutes
**Dependencies**: None

**Acceptance Criteria**:
- GitHub Secrets configured
- Test email received

### Subtasks
- [ ] 1.1 Get Gmail app password from https://myaccount.google.com/apppasswords
- [ ] 1.2 Add EMAIL_HOST secret (smtp.gmail.com)
- [ ] 1.3 Add EMAIL_PORT secret (587)
- [ ] 1.4 Add EMAIL_USER secret
- [ ] 1.5 Add EMAIL_PASS secret (app password)
- [ ] 1.6 Add EMAIL_TO secret
- [ ] 1.7 Run manual workflow test
- [ ] 1.8 Verify email delivery

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
