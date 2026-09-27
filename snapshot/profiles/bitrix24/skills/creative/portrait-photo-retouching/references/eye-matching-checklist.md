# Eye-matching checklist

Use this reference for a localized bilateral eye correction in a portrait.

## Coordinate convention

- Always label sides twice: `subject-left/viewer-right` and `subject-right/viewer-left`.
- Do not use bare “left” or “right” in working notes or filenames.
- Detect whether the image has been mirrored before choosing the target.

## Measurements before editing

Record for both eyes:

1. inner and outer canthus coordinates;
2. visible aperture width;
3. maximum aperture height;
4. upper- and lower-lid curvature;
5. iris diameter and center;
6. visible sclera on nasal and temporal sides;
7. eye-center angle relative to the face;
8. distance to spectacle rims, when present.

Measure the visible eye itself, not the glasses lens or surrounding crop. A donor patch may include feathering margin, but its transformed eye aperture must match the target geometry.

## Compositing sequence

1. Start from the untouched original.
2. Crop only the donor eye aperture plus a narrow margin.
3. Mirror only when required by side.
4. Transform to the measured target width, height, center, and angle.
5. Use a strong mask over iris, sclera, and eyelids when exact matching is requested.
6. Feather only the perimeter; broad translucent blending can leave the old eye visible underneath and create double lids or excess sclera.
7. Keep eyebrow, glasses rim, cheek, and nose outside the mask.
8. Match local tone only after geometry is correct.

## Verification gates

At 200–400% crop:

- compare eye width and height numerically;
- compare lid contours;
- compare sclera area and distribution;
- confirm equal iris/pupil size and aligned gaze;
- inspect for seams, halos, duplicated lashes, double lids, or frame damage.

At normal full-image size:

- confirm neither eye appears larger;
- confirm the expression and identity are unchanged;
- confirm the edit does not draw attention.

If any gate fails, discard the derivative and restart from the original rather than layering another correction.
