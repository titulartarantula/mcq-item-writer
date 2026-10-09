# Using media in items

Source: NBME Item-Writing Guide, Ch 7 [NBME pp. 56–66]. Generalised from clinical media to any domain.

## Contents
- Why use media
- Choosing media
- Types of media
- Areas where media add most
- Writing the stem around media
- Acquiring and creating media
- Video production tips
- Accessibility
- Media specification block (for this skill)

## Why use media

Media can [NBME p. 56]:
- make the assessment more **authentic**: the learner sees or hears the thing instead of reading a description
- assess skills that text can't capture well, such as recognising a visual pattern, judging tone, or reading an instrument
- **avoid textual cues.** A long written description of an appearance often contains the very words that reveal the answer, and an image avoids that

Media must be **chosen on purpose** to help answer the question. Otherwise it is just extra material [NBME p. 59].

## Choosing media

Consider [NBME p. 56]:
- **Fit to the skill.** Choose the medium that best simulates how the learner meets this information in practice: a screenshot of an error dialog, a photo of a defect, a chart from a report, an audio clip of a customer call.
- **Novelty.** Unfamiliar media types or interactions may need a tutorial. Simple access is usually better.
- **Memorability.** Distinctive images get remembered and shared between cohorts ("the photo with the red truck is the brake-failure one"). Write **several items for each media asset** and rotate them.
- **Richness and time.** Rich media (long video, interactive simulation) adds authenticity but also time on task. Budget for it in the test length.

## Types of media

[NBME p. 56], generalised:
- static images: photos, screenshots, diagrams, charts, documents, maps
- video: procedures, interactions, demonstrations
- audio: calls, machine sounds, spoken language
- interactive: simulations, hotspot exploration, avatars

## Areas where media add most

Media help most where a text description would be awkward or would give the answer away [NBME pp. 60–61]:
- visual inspection (defects, damage, visual patterns, layouts)
- auditory recognition (sounds, speech, tone)
- procedures and physical technique
- **communication and ethics.** Text-only versions tend to be easy because tone, intonation, and body language are missing. Video of the interaction makes the judgment authentic.

## Writing the stem around media

- **Don't describe in text what the media already shows** [NBME p. 59]. If the image shows the defect, the stem says "A photograph of the weld is shown", not "The weld shows porosity and undercut."
- The item must **not be answerable from the media alone, or from the text alone**, if the intent is that both are needed [NBME p. 69].
- The lead-in and options follow all the usual rules. Media doesn't excuse flaws.

## Acquiring and creating media

[NBME pp. 62–63]
- **Confidentiality and consent.** Remove anything that identifies people, organisations, or places, unless it is needed. Get signed consent for any identifiable person. Follow your institution's privacy policy.
- **Metadata.** Record it at acquisition so assets can be found and reused: description, keywords, what it depicts, normal or abnormal, source, rights and licence, consent status, a descriptive file name, and clip in/out points with an audio-relevance flag for video. *Media are only as useful as their metadata.*
- **Sources.** Options are your own or subject-matter experts' libraries (watch confidentiality and memorability), vendors (costly but customisable), or new production with actors.
- **Formats.** Get media in the format your delivery platform needs, rather than converting. Don't use images pulled out of slide decks or documents, or screenshots of published images: quality drops and copyright is unclear.
- **Diversity.** Show the same phenomenon across different people and contexts (see `people-in-scenarios.md`).

## Video production tips

[NBME p. 64], generalised. Every unplanned visual detail is a possible cue, a distraction, and a memory hook.

**Do**
- use a plain background with no identifiable décor or equipment
- light the room well
- dress people plainly: no logos, bright colours, or jewellery
- keep background and clothing consistent across clips in a series
- have people speak naturally, as they would in a real interaction, without using names
- keep clips to about **30 seconds**
- deliver raw footage with editing instructions
- get signed consent

**Don't**
- use a distinctive room, wall art, or unusual furniture
- show faces unless faces are essential
- add narration that explains what is happening
- add transitions (fades), or resize or re-encode needlessly

## Accessibility

Plan accessibility **from the start**. Retrofitting it is harder [NBME p. 65].

**Hearing**
- captions or subtitles for any video with meaningful audio
- for non-speech audio that must be interpreted, provide a synchronised visual representation (for example, a waveform)

**Vision**
- **alt text or a text description** for every image. ⚠ The description must give equivalent access **without cueing the answer**. Describe what is visible, not what it means. Too much interpretation gives screen-reader users an unfair advantage [NBME p. 65].
  - ✗ "Photo showing a cracked weld caused by hydrogen embrittlement"
  - ✓ "Close-up photo of a steel weld seam about 10 cm long with a thin dark line running along its centre"
- **Colour**: prefer black and greys. Never rely on red versus green alone. Use patterns or textures in charts and keep colour as a secondary cue [NBME pp. 65–66].
- **Text in images**: sans-serif font, at least 8 pt, or allow zooming [NBME p. 66].

> Beyond the guide: for web delivery, also aim for WCAG 2.2 AA: text contrast of at least 4.5:1, keyboard-operable media controls, and no auto-playing audio.

## Media specification block (for this skill)

The skill doesn't create media. When an item would benefit from media, it outputs a specification that a media producer or subject-matter expert can act on:

```json
"media": {
  "type": "image | video | audio | interactive",
  "purpose": "why this medium beats a text description for this testing point",
  "depicts": "what must be visible or audible (factual, no interpretation)",
  "must_not_show": ["identifying details", "cues to the key"],
  "alt_text": "non-cueing description for screen readers",
  "captions_required": true,
  "notes": "colour, duration, consistency requirements"
}
```

Where media is specified, the stem refers to it ("A screenshot of the error is shown.") and doesn't repeat its content in words.
