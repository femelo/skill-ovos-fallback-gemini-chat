# Gemini Chat Fallback Skill

When in doubt, ask Gemini Chat, powered by [Gemini Chat Solver](https://github.com/femelo/ovos-solver-plugin-gemini-chat).

You need to configure an API key for your [Gemini](https://gemini.google.com) account.

## About

Capabilities:

- Remembers what user said earlier in the conversation
- Can augment the answer with web content
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content

## Configuration

Under skill settings (`~/.config/mycroft/skills/skill-ovos-fallback-gemini-chat.femelo/settings.json`) you can tweak some parameters for Gemini Chat.

| Option             | Value                                                                  | Description                             |
| ------------------ | ---------------------------------------------------------------------- | --------------------------------------- |
| `api_key`          | `your-gemini-api-key`                                                  | Your Gemini API key                     |
| `persona`          | `You are a helpful assistant who gives very short but factual answers` | Give a personality to a Gemini model    |
| `model`            | `gemini-2.5-flash`                                                     | LLM model to use                        |
| `enable_reasoning` | `false`                                                                | Enable dynamic thinking by the model    |
| `name`             | `AI assistant`                                                         | Name to give to the AI assistant        |
| `confirmation`     | `true`                                                                 | Spoken confirmation                     |

Read more about it in the OVOS technical manual, page [persona server](https://openvoiceos.github.io/ovos-technical-manual/persona_server/#compatible-projects)

The default persona is `You are a helpful voice assistant with a friendly tone and fun sense of humor. You respond in 40 words or fewer`

## Configurations

The skill utilizes the `~/.config/mycroft/skills/skill-ovos-fallback-gemini-chat.femelo/settings.json` file which allows you to configure it.

### Configuration for use with Gemini Chat

```json
{
  "api_key": "{your-gemini-api-key}",
  "model": "gemini-2.5-flash",
  "persona": "You are a helpful voice assistant with a friendly tone and fun sense of humor",
  "enable_reasoning": false,
  "__mycroft_skill_firstrun": false
}
```

## Examples

- "Explain quantum computing very briefly"
- "Got any creative ideas for a 10 year old’s birthday?"
