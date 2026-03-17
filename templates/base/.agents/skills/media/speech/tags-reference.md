# ElevenLabs Audio Tags Reference

Complete reference for audio tags supported by ElevenLabs Eleven v3. Tags are enclosed in square brackets and guide delivery without being spoken aloud.

## Emotions

### Primary Emotions
`[happy]`, `[sad]`, `[angry]`, `[scared]`, `[surprised]`, `[disgusted]`

### Emotional States
`[excited]`, `[nervous]`, `[frustrated]`, `[anxious]`, `[calm]`, `[relaxed]`, `[tense]`, `[relieved]`, `[hopeful]`, `[hopeless]`, `[confident]`, `[insecure]`, `[proud]`, `[ashamed]`, `[guilty]`, `[jealous]`, `[envious]`, `[grateful]`, `[content]`, `[bored]`, `[curious]`, `[confused]`, `[determined]`, `[defeated]`, `[nostalgic]`, `[melancholic]`, `[sorrowful]`, `[bitter]`, `[resentful]`

### Emotional Intensity
`[slightly sad]`, `[very angry]`, `[extremely excited]`, `[mildly annoyed]`

## Delivery & Tone

### Volume
`[whispers]`, `[quietly]`, `[softly]`, `[normal volume]`, `[loudly]`, `[shouts]`, `[screams]`, `[yells]`, `[murmurs]`, `[mutters]`

### Pacing
`[slowly]`, `[quickly]`, `[rushed]`, `[measured pace]`, `[drawn out]`, `[clipped]`, `[leisurely]`, `[urgently]`

### Tone Quality
`[cheerfully]`, `[flatly]`, `[deadpan]`, `[playfully]`, `[seriously]`, `[sarcastically]`, `[mockingly]`, `[sincerely]`, `[warmly]`, `[coldly]`, `[harshly]`, `[gently]`, `[tenderly]`, `[bitterly]`, `[sweetly]`, `[dryly]`, `[matter-of-factly]`

### Character Attitudes
`[dismissively]`, `[condescendingly]`, `[humbly]`, `[arrogantly]`, `[timidly]`, `[boldly]`, `[cautiously]`, `[recklessly]`, `[thoughtfully]`, `[carelessly]`, `[respectfully]`, `[rudely]`

## Speech Patterns

### Hesitation & Uncertainty
`[hesitates]`, `[stammers]`, `[stutters]`, `[trails off]`, `[falters]`, `[uncertain]`, `[indecisive]`, `[searching for words]`

### Emphasis & Stress
`[emphasized]`, `[understated]`, `[stress on next word]`, `[dramatic pause]`

### Rhythm
`[pause]`, `[long pause]`, `[brief pause]`, `[beat]`, `[pauses for effect]`

## Human Reactions

### Vocal Reactions
`[laughs]`, `[chuckles]`, `[giggles]`, `[snickers]`, `[cackles]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[snorts]`

`[sighs]`, `[exhales]`, `[inhales sharply]`, `[gasps]`, `[gulps]`, `[swallows]`, `[clears throat]`, `[coughs]`, `[sneezes]`, `[yawns]`, `[groans]`, `[moans]`, `[whimpers]`, `[sobs]`, `[cries]`, `[sniffles]`, `[hiccups]`

### Non-Verbal Sounds
`[tsk]`, `[hmm]`, `[uh]`, `[um]`, `[ah]`, `[oh]`, `[oof]`, `[phew]`, `[wow]`, `[huh]`, `[mhm]`, `[uh-huh]`, `[nuh-uh]`, `[shh]`, `[psst]`

## Conversation Flow

### Turn-Taking & Interruptions
`[interrupting]`, `[overlapping]`, `[starting to speak]`, `[cuts in]`, `[talks over]`, `[jumps in]`, `[interjects]`

These tags affect delivery style (rushed entry, natural transitions) but audio remains sequential — no true simultaneous speech. Use em dash for cut-off effect:
```json
{"speaker": "alice", "text": "I really think we should—"},
{"speaker": "bob", "text": "[interrupting] —exactly what I was thinking!"}
```

### Response Patterns
`[responds quickly]`, `[responds slowly]`, `[hesitates before responding]`, `[reluctantly]`, `[eagerly]`

### Self-Correction
`[self-interrupt]`, `[catches self]`, `[corrects self]`, `[backpedals]`

## Sound Effects

### Environment
`[footsteps]`, `[door knock]`, `[door creaks]`, `[door slams]`, `[phone rings]`, `[clock ticking]`, `[rain]`, `[thunder]`, `[wind]`, `[birds chirping]`, `[crickets]`, `[leaves rustling]`

### Actions
`[applause]`, `[clapping]`, `[typing]`, `[writing]`, `[paper rustling]`, `[glass breaking]`, `[splash]`

### Dramatic
`[explosion]`, `[gunshot]`, `[crash]`, `[thud]`, `[bang]`, `[whoosh]`

## Character Direction

### Accents
`[British accent]`, `[American accent]`, `[Southern accent]`, `[New York accent]`, `[Irish accent]`, `[Scottish accent]`, `[Australian accent]`, `[French accent]`, `[German accent]`, `[Russian accent]`, `[Italian accent]`, `[Spanish accent]`, `[Indian accent]`, `[Japanese accent]`

Use `[strong X accent]` or `[slight X accent]` for intensity.

### Character Types
`[narrator]`, `[storyteller]`, `[news anchor]`, `[radio host]`, `[announcer]`, `[auctioneer]`, `[teacher]`, `[professor]`, `[doctor]`, `[military]`, `[robot]`, `[villain]`, `[hero]`

### Performance Styles
`[theatrical]`, `[naturalistic]`, `[over-the-top]`, `[subtle]`, `[melodramatic]`, `[understated]`

## Singing & Music

`[sings]`, `[hums]`, `[whistles]`, `[beatboxes]`, `[raps]`

## Combining Tags

Tags can be combined for complex delivery:
- `[whispers][scared] Did you hear that?`
- `[laughs][nervously] That's... that's not funny.`
- `[slowly][sadly] I never got to say goodbye...`
- `[interrupts][excitedly] Wait, I just figured it out!`

## Best Practices

1. **Use sparingly** — Tags at key emotional beats, not every line
2. **Match voice to tags** — Choose voices with emotional range for complex scenes
3. **Combine punctuation** — Em dash (—) for interrupts, ellipsis (...) for trailing
4. **Layer emotions** — Combine emotion + delivery for nuance
5. **Test and iterate** — Tags are interpreted, results may vary
