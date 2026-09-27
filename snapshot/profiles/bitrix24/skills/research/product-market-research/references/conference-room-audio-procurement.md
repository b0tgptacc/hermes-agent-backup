# Conference-room audio procurement

Use this note when researching corporate meeting-room audio for echo, self-hearing, or reverberation complaints.

## Diagnose the requirement

- Remote participants hearing themselves points to acoustic echo in the loudspeaker→room→microphone loop. Require explicit AEC or written confirmation of reference-based echo cancellation.
- Noise suppression is not AEC. It mainly targets HVAC, keyboard, projector, and steady background noise.
- Long room reverberation needs dereverberation/room EQ and often physical acoustic treatment; do not promise that a portable speakerphone will fix a reflective room.
- A ceiling microphone is not necessarily a complete system. Confirm DSP/AEC, far-end reference routing, USB/codec interface, amplifier, loudspeakers, PoE/networking, installation, and commissioning.

## Russian-market availability evidence

Use exact Russian product pages, not marketplace search snippets. Record one of these statuses verbatim:

1. `confirmed stock` — page explicitly says in stock or gives a numeric quantity;
2. `conflicting status` — e.g. both “in stock” and “made to order” appear;
3. `active offer, stock unconfirmed` — buy button/price exists but no quantity;
4. `quote only` — no public price or stock;
5. `unavailable` — out of stock/discontinued.

Never collapse an active card into “in stock.” Preserve seller caveats such as “confirm price and availability with manager.” Sort the procurement shortlist by stock confidence before technical preference when the user explicitly requires immediate Russian availability.

## Technical evidence hierarchy

- Official datasheet/manual governs AEC, full duplex, pickup radius, supported room size, interfaces, and expansion.
- Russian seller page governs local price, VAT wording, stock, delivery, and warranty.
- If a manufacturer says only `echo reduction`, do not relabel it `AEC`; require a pilot or written vendor confirmation.
- Distinguish room dimensions from Bluetooth range and distinguish call-party count from physical room participants.

## Visual shortlist workflow

When the user asks for a document with pictures:

1. Keep the requested section(s) only; do not preserve the full research narrative.
2. Download product images from the exact seller page (`og:image` is a practical source) or the official manufacturer.
3. Preserve image provenance in the caption or source section.
4. Convert WebP to PNG/JPEG before embedding when the document library cannot consume WebP reliably.
5. Present each product as a card: image, price, stock status, room fit, decisive features, limitation, seller, URL.
6. Use explicit stock-confidence labels and visual status colors, but repeat the meaning in text for accessibility.
7. Re-extract embedded images and validate the DOCX package before delivery.

## Pilot acceptance test

- Only one room audio endpoint joins the call.
- Start with USB rather than Bluetooth.
- Feed far-end speech through the room loudspeakers and verify it does not return to the far end.
- Verify full duplex with simultaneous near/far speech.
- Test farthest seats plus HVAC/projector noise.
- For installed systems, verify that the AEC receives the same far-end reference sent to the loudspeakers.
