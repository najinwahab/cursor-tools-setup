# Setting up Cursor IDE with AI agent extensions: Claude Code and Codex

## Tools Installed
- Cursor IDE (downloaded from cursor.com)
- Codex extension (installed via Cursor Extensions, logged in)
- Claude Code extension (installed, but login requires a paid Claude Pro/Max plan — 
  I was unable to log in due to this requirement at this time)

## Steps Completed
1. Downloaded and installed Cursor IDE
2. Searched for and installed "Claude Code" extension
3. Searched for and installed "Codex" extension — successfully logged in
4. Created a public GitHub repository
5. Opened the repository in Cursor IDE
6. Created and edited this README.md file
7. Committed and pushed to GitHub

## Issues Encountered
- **Claude Code login**: The extension requires an active Claude Pro or Max subscription 
  to authenticate. I currently do not have a paid plan. I documented this honestly 
  rather than skipping the step, as the task instructions encouraged transparency 
  about obstacles faced.
- **Cursor basics**: Watched some YouTube videos to learn how to use cursor and applied. 
- **Git/GitHub experience**: First time using GitHub — learned the process through YouTube tutorials and GitHub's official documentation.
- **Repository creation**: Utilized Perplexity AI to learn creating GitHub respository step-by-step.

---

## Phase 2: Research Collection

### Topic Chosen
**AI-Powered SEO Content Production**

### Why This Topic
AI is fundamentally reshaping how content is created, distributed, and 
discovered through search. The experts in this list are not commentators — 
they are practitioners actively building tools, frameworks, and methodologies 
that define this shift. Collecting their content creates a high-signal 
foundation for building a real playbook on AI-powered SEO content production.

---

## Experts Selected

| Expert | Role / Affiliation | Why Chosen |
|---|---|---|
| Lily Ray | VP SEO, Amsive | Leading voice on GEO, AEO, and AI search accuracy; backed by real platform data |
| Michael King | Founder, iPullRank | Most technically rigorous SEO practitioner; coined Relevance Engineering |
| Ryan Law | Content Strategist, Ahrefs | Original research on LLM citations, AI traffic, and content quality thresholds |
| Aleyda Solis | International SEO Consultant | Pioneer of AI search checklists and the SEOFOMO research reports |
| Jason Barnard | Founder, Kalicube | Creator of the Brand SERP and DSCRI-ARGDW AI pipeline framework |
| Kevin Indig | Growth Advisor | Growth Memo newsletter; bridges SEO, product, and AI systems thinking |
| Koray Tuğberk Gübür | Founder, Holistic SEO | Coined Topical Authority; most cited semantic SEO framework in the industry |
| Ross Simmonds | Founder, Foundation Marketing | Pioneer of AI-powered content distribution; creator of Distribution.ai |
| Britney Muller | AI/ML Consultant, ex-Moz | First to document NLP and entity-based SEO at Moz; now focuses on ML for marketers |
| Brian Dean | Founder, Backlinko | Creator of the Skyscraper Technique; authority on data-driven content strategy |

---

## Repository Structure

- `research/`
  - `linkedin-posts/` — 3 recent LinkedIn posts per expert (10 files)
  - `youtube-transcripts/` — 1 full YouTube transcript per expert (10 files)
  - `other/` — Supplementary articles, guides, and research (10 files)
  - `sources.md` — Master list of all sources with links and annotations


---

## Challenges & Resolutions

### YouTube Transcript Collection
- **Inactive or low-reach personal channels**: Some experts have personal YouTube 
  channels that are either inactive or have very low viewership. For example, 
  Ross Simmonds has a YouTube channel but his video view counts are too low to 
  represent his best thinking. In these cases, I identified other channels — 
  podcasts, conference recordings, or interview series — where these experts 
  were featured as guests and delivered high-quality insights.
- **No personal YouTube channel**: Some experts such as Ryan Law do not operate 
  a personal YouTube channel at all. I applied the same method — finding podcast 
  episodes and interviews where they appeared on established channels — to source 
  the most relevant and high-quality transcript available.
- **Solution**: Every transcript selected is evaluated on content quality and 
  relevance to AI-powered SEO, not on whether it comes from the expert's own 
  channel.

### Other Folder — Supplementary Materials
- **Third-party authored content**: For some experts, the most valuable 
  supplementary material was not always authored directly by them. For example, 
  both web resources collected for Britney Muller are authored by other writers 
  but feature her presence, insights, and direct contributions — such as Moz 
  Whiteboard Friday appearances and written interviews. The same method was 
  applied to other experts where appropriate.
- **Solution**: Every file in the `/other/` folder is clearly annotated with the 
  original author, source, URL, document type, and a summary explaining why it 
  was selected and what it contributes to the research.

- **YouTube transcript extraction via API**: Attempted to automate transcript 
  Despite multiple debugging attempts using Codex, the script returned a 403 
  Access Denied error (Cloudflare Error 1010 — browser signature banned), 
  meaning the API blocked the automated request at the infrastructure level. 
  This was not resolvable through code fixes alone.
- **Solution**: As a workaround, I used the Supadata web interface directly to manually collect 
  all transcripts — ensuring the task was completed to the required standard 
  while being transparent about the technical obstacle encountered.
---

## Commit Practice
Commits were made regularly throughout the research — after each expert's 
LinkedIn posts, after each YouTube transcript, and after each supplementary 
material file — rather than in one large batch at the end. This reflects a 
genuine working process and makes the contribution history easy to follow.

