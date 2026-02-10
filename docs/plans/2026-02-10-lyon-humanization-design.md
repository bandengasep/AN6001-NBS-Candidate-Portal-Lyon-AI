# Lyon Humanization Design

**Date:** 2026-02-10
**Goal:** Make Lyon's responses feel like chatting with a real person -- concise, conversational, no information dumps.

## Problems

1. **Information overload**: Lyon dumps everything the RAG tool returns instead of answering the question directly. Responses are 3-4 paragraphs when 1-2 sentences would suffice.
2. **Formatting breaks the chat illusion**: Bullet points, numbered lists, and markdown headers make responses look like documents, not messages. The `.markdown-content` CSS adds `margin-left: 1.5rem` to lists, causing visible indentation in chat bubbles.

## Approach: Triple-Layer Fix

Three independent layers, each backstopping the others:

### Layer 1: System Prompt Rewrite

Replace the VOICE RULES and add a RESPONSE FORMAT section to the system prompt. Keep all other sections (IDENTITY, TOOL USAGE, ALLOWED TOPICS, OFF-TOPIC, SECURITY, BOUNDARIES) unchanged.

**New VOICE RULES:**

```
VOICE RULES:
- Use Singlish for greetings, transitions, and encouragement -- not for factual content
- When delivering programme details, be precise and clear in standard English
- If the user writes casually, match their energy. If they write formally, dial back the Singlish slightly
```

**New RESPONSE FORMAT section (add after VOICE RULES):**

```
RESPONSE FORMAT:
- For initial answers: keep it to 2-4 sentences. Give the most relevant fact, then offer to go deeper
- When the user asks you to elaborate or says "tell me more": you can give a fuller response (up to a short paragraph), but still write in flowing sentences -- no bullet lists
- NEVER use bullet points, numbered lists, markdown headers, or code blocks
- NEVER dump all available information at once, even if your tools return a lot of data. Curate and summarize
- Write in natural flowing sentences like you're texting a friend, not writing a report
- Bold text for emphasis is fine. Links are fine. Everything else is not
- If you need to mention multiple items, weave them into a sentence naturally instead of listing them
- When a question is broad ("Tell me about the MBA"), ask what aspect matters most instead of covering everything
```

**Updated EXAMPLE PHRASES:**

```
EXAMPLE PHRASES (for tone calibration only -- vary your language naturally):
- Greeting: "Hey! Welcome to NBS. I'm Lyon, NTU's resident lion. What programme are you eyeing?"
- Encouragement: "Wah, good choice! That programme is really popular."
- Transition: "Okay let me check that for you ah..."
- Factual (drip-feed): "For the Nanyang MBA, the big three are a bachelor's degree, at least 2 years of work experience, and a competitive GMAT score. Want me to go deeper into any of these?"
- Comparison (drip-feed): "The main difference between MSc Financial Engineering and MSc Accountancy is the career track -- one targets quant roles, the other audit and advisory. Want me to break down the specifics?"
- Broad question: "There's quite a bit to cover on that one! What's most important to you -- the fees, the curriculum, or the admissions requirements?"
- Uncertainty: "Hmm, I'm not 100% sure on that one. Better check the NBS website or drop them an email lah."
- Sign-off: "Anything else you want to know? I'm here lah."
```

### Layer 2: GPT-5.2 Verbosity Parameter

Pass `text.verbosity: "low"` via `model_kwargs` when initializing `ChatOpenAI`. This constrains the model's token budget at the API level, independent of prompt instructions.

**File:** `backend/app/agents/nbs_agent.py`

```python
self.llm = ChatOpenAI(
    model=settings.chat_model,
    temperature=0.7,
    api_key=settings.openai_api_key,
    model_kwargs={"text": {"verbosity": "low"}}
)
```

**Rationale:**
- Default is `"medium"`, which is what Lyon currently produces
- `"low"` tells the model to be concise with minimal commentary
- The prompt can still steer longer responses when the user asks to elaborate
- If `model_kwargs` doesn't pass through cleanly in the current LangChain version, this is a harmless no-op

### Layer 3: Frontend Markdown Filtering

**3a. Restrict ReactMarkdown allowed elements**

In `MessageBubble.jsx`, configure `ReactMarkdown` to only render `<p>`, `<strong>`, `<em>`, `<a>`, and `<br>`. All other elements (headers, lists, code blocks) are unwrapped to plain text:

```jsx
<ReactMarkdown
  allowedElements={['p', 'strong', 'em', 'a', 'br']}
  unwrapDisallowed={true}
>
  {content}
</ReactMarkdown>
```

**3b. Simplify `.markdown-content` CSS**

In `frontend/src/index.css`, remove styles for:
- `h1`, `h2`, `h3` (headers)
- `ul`, `ol`, `li` (lists -- source of indentation bug)
- `code` (code blocks)

Keep only:
- `p { margin-bottom: 0.5rem }` (tighter than current 0.75rem)
- `a` colors (NBS red)
- Bold stays as browser default

**3c. No changes to `splitIntoBubbles()`**

Shorter responses will naturally produce fewer bubbles. The existing split-on-double-newline logic works fine.

## Files to Modify

| File | Change |
|------|--------|
| `backend/app/agents/nbs_agent.py` | Rewrite system prompt + add `model_kwargs` |
| `frontend/src/components/Chat/MessageBubble.jsx` | Add `allowedElements` and `unwrapDisallowed` to ReactMarkdown |
| `frontend/src/index.css` | Simplify `.markdown-content` styles |

## What Stays the Same

- Lyon's Singlish personality (IDENTITY section unchanged)
- Topic fencing and off-topic handling
- Security / anti-injection rules
- Tool usage (RAG, compare, FAQ)
- Agent architecture (LangChain, middleware, recursion limits)
- Conversation history handling
- File upload / CV parsing
- All other frontend components and routes

## Testing

After implementation, manually test these scenarios:
1. Simple greeting ("Hi!") -- should get 1-2 sentence response
2. Specific question ("What are MBA requirements?") -- 2-4 sentences + offer to elaborate
3. Follow-up ("Tell me more about GMAT") -- fuller paragraph in prose, no lists
4. Broad question ("Tell me about NBS") -- should ask what aspect matters
5. Comparison ("Compare MBA and MFE") -- short comparison + offer details
6. Off-topic ("What's the weather?") -- unchanged redirect behavior
7. Verify no bullet points, headers, or code blocks appear in any response
