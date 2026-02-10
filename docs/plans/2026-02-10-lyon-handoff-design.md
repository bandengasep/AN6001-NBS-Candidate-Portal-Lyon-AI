# Lyon Advisor Hand-off Design

**Date:** 2026-02-10
**Goal:** Let Lyon connect users with a (simulated) NBS advisor when it can't answer a question or the user requests a 1-on-1 session. Demo feature for class project presentation.

## How It Works

1. Lyon detects a knowledge gap or the user asks to speak with someone
2. Lyon calls the `schedule_advisor_session` tool
3. The backend detects the tool call and adds `show_handoff_form: true` to the API response
4. The frontend renders an inline form card in the chat (name, email, topic)
5. User submits the form, sees a confirmation -- all within the chat flow

## Backend Changes

### New file: `backend/app/agents/tools/handoff.py`

A LangChain tool named `schedule_advisor_session`. When called, returns a short string that gives Lyon context to respond naturally (e.g. "Advisor session request noted. Let the student know the form will appear shortly."). The tool's main purpose is to act as a signal, not to perform real scheduling.

### Modify: `backend/app/agents/nbs_agent.py`

**Add tool to toolkit:**
```python
from app.agents.tools import create_handoff_tool

self.tools = [
    create_rag_tool(),
    create_compare_tool(),
    create_faq_tool(),
    create_handoff_tool()
]
```

**Detect tool call after agent runs:**

After extracting the response from `result["messages"]`, scan for any tool call to `schedule_advisor_session`:

```python
handoff_triggered = False
if "messages" in result:
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls"):
            for tc in msg.tool_calls:
                if tc.get("name") == "schedule_advisor_session":
                    handoff_triggered = True
                    break
```

**Include flag in response:**
```python
return {
    "response": response,
    "conversation_id": conversation_id,
    "sources": [],
    "show_handoff_form": handoff_triggered
}
```

**System prompt -- add HAND-OFF section after TOOL USAGE:**
```
HAND-OFF:
- If you searched the knowledge base and genuinely cannot find the answer, offer to connect the user with an NBS advisor. Say something like: "I don't have that info on hand, but I can connect you with an NBS advisor who can help. Want me to set that up?"
- If the user explicitly asks to speak with someone, talk to an advisor, schedule a session, or says anything like "can I talk to a real person", call the schedule_advisor_session tool immediately
- When handing off, call the schedule_advisor_session tool -- this will show the user a form to fill in their details
- Do NOT try to collect the user's name, email, or details yourself -- the form handles that
- After calling the tool, let the user know an advisor form will appear and they can fill it in
- Only offer hand-off for genuine knowledge gaps -- do NOT offer it for off-topic questions (those get the standard redirect)
```

**Tool description (visible to Lyon):**
```
schedule_advisor_session: Use this when the user wants to speak with a real NBS advisor or when you cannot find the information they need in the knowledge base. This will show the user a form to schedule a 1-on-1 session.
```

### Modify: `backend/app/api/routes/chat.py`

Add `show_handoff_form: bool = False` to the `ChatResponse` Pydantic model.

### New endpoint: `POST /api/chat/handoff`

Accepts `{name: str, email: str, topic: str, conversation_id: str}`. For demo purposes, returns:
```json
{"status": "success", "message": "Your session has been scheduled. An NBS advisor will reach out to you shortly."}
```

No database storage -- just a success response.

## Frontend Changes

### New component: `frontend/src/components/Chat/HandoffCard.jsx`

An inline card rendered inside the chat flow. Visually distinct from regular chat bubbles (subtle border or accent color) but matching the existing design language.

**Form state:**
- Name (text input, required)
- Email (email input, required)
- Preferred topic/concern (text input, optional)
- Submit button (NBS red)

**States:**
1. **Form**: Shows the three inputs + submit button
2. **Submitting**: Button shows loading state
3. **Success**: Card transforms into a confirmation message ("All set! An NBS advisor will reach out to you at {email}.")

**Styling:**
- Rounded card with light border
- Same max-width as chat bubbles
- Left-aligned (like assistant messages)
- Fade-in animation matching existing messages

### Modify: `frontend/src/hooks/useChat.js`

When API response includes `show_handoff_form: true`, append a special message:
```js
if (response.show_handoff_form) {
  assistantMessages.push({
    id: now + bubbles.length + 1,
    role: 'handoff',
    content: '',
    timestamp: new Date().toISOString(),
  });
}
```

### Modify: `frontend/src/components/Chat/MessageList.jsx`

When rendering messages, check for `role === 'handoff'` and render `<HandoffCard />` instead of `<MessageBubble />`.

### Modify: `frontend/src/services/api.js`

Add a `submitHandoff(name, email, topic, conversationId)` function that POSTs to `/api/chat/handoff`.

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `backend/app/agents/tools/handoff.py` | Create | New `schedule_advisor_session` tool |
| `backend/app/agents/tools/__init__.py` | Modify | Export `create_handoff_tool` |
| `backend/app/agents/nbs_agent.py` | Modify | Add tool, detect tool call, add prompt section |
| `backend/app/api/routes/chat.py` | Modify | Add `show_handoff_form` to response model, add handoff endpoint |
| `frontend/src/components/Chat/HandoffCard.jsx` | Create | Inline form card component |
| `frontend/src/components/Chat/MessageList.jsx` | Modify | Render HandoffCard for `role === 'handoff'` |
| `frontend/src/hooks/useChat.js` | Modify | Detect `show_handoff_form` flag, add handoff message |
| `frontend/src/services/api.js` | Modify | Add `submitHandoff` API call |

## What Stays the Same

- All existing chat functionality (messages, history, file upload)
- Lyon's personality and Singlish voice
- Off-topic handling (redirect, don't offer advisor)
- Security rules
- Other pages (splash, recommend, programmes)

## Testing

1. **Knowledge gap**: Ask Lyon something not in the knowledge base (e.g. specific faculty office hours) -- should offer advisor hand-off
2. **User request**: Say "I want to talk to a real advisor" -- should trigger form immediately
3. **Off-topic**: Ask about weather -- should get standard redirect, NOT advisor offer
4. **Form submission**: Fill in form, submit -- should show success confirmation
5. **Form validation**: Submit empty form -- should show validation errors
6. **Multiple hand-offs**: Trigger hand-off twice in one conversation -- both should work independently
