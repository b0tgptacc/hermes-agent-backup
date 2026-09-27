# Image-backed PowerPoint pattern

Use this pattern when the user prioritizes polished, deterministic visuals over native text editing.

## Build pattern

1. Render every slide at 1920×1080 using one shared design system.
2. Save deterministic PNGs with stable numbering: `slide-01.png`, `slide-02.png`, and so on.
3. Create a 16:9 PowerPoint deck with blank layouts.
4. Place each PNG at `(0, 0)` sized to the full slide.
5. Set title, subject, author, and keywords in document properties.
6. On the source slide, add transparent rectangle shapes over URL rows and assign external hyperlinks to their click actions.
7. Save the generator, PNGs, contact sheet, research brief, citation ledger, and final `.pptx` together.

## Why it works

- The exact reviewed pixels are the pixels displayed in PowerPoint.
- Font substitution cannot reflow text inside the slide image.
- Visual comparison and regression checks are deterministic.
- Source links can remain clickable despite the image background.

## Limitations

- Text, charts, and cards inside the PNG are not individually editable.
- Accessibility and text extraction are weaker than in a native deck.
- Hyperlinks require explicit overlay shapes.
- Speaker notes and semantic slide structure must be added separately if required.
- Large decks can become media-heavy.

Disclose these limitations before calling the deck editable.

## Verification

- Build a contact sheet from the exact slide PNGs.
- Review dense slides individually at full resolution.
- Read the `.pptx` back and require one full-slide image per slide.
- Inspect the source slide relationship file or deck outline and count external hyperlinks.
- Confirm slide count, size, file size, and checksum.
- If no Office renderer is available, say so; image-backed output still permits exact inspection of the embedded visuals, but not an Office-engine compatibility claim.
