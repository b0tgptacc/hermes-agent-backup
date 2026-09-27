---
name: portrait-photo-retouching
description: "Use when retouching faces or eyes in existing photos."
version: 1.0.0
tags: [photo-editing, portrait, retouching, eyes, identity-preservation]
---

# Portrait Photo Retouching

Use this skill for localized corrections to a real person's face in an existing photograph: eyes, eyelids, gaze, minor asymmetry, skin blemishes, stray hairs, and similar edits where identity preservation matters.

## Core principle

Make the smallest edit that satisfies the request. Preserve identity, facial proportions, expression, glasses, lighting, skin texture, image dimensions, and all unaffected regions.

## Required workflow

1. **Resolve anatomical orientation before editing.**
   - “Left eye” normally means the subject's anatomical left eye, which appears on the viewer's right in a frontal photograph.
   - State the mapping internally as `subject-left = viewer-right` and `subject-right = viewer-left`.
   - If the image is mirrored, profile, or ambiguous, inspect landmarks before choosing the target.
2. **Inspect at two scales.**
   - View the entire portrait for pose and expression.
   - Inspect a tight crop containing both eyes so their width, height, lid curvature, iris size, sclera exposure, gaze, and spectacle geometry can be compared.
3. **Use the untouched original as the source for every revision.** Never compound edits by editing an already edited derivative.
4. **Measure before copying or warping.** Record source and target eye centers, visible eye width/height, canthus positions, and vertical offset. Do not size a patch from the lens or surrounding skin region.
5. **Prefer subtle local correction.** Copy/warp only the eyelids, iris, and sclera required to match the reference eye. Exclude eyebrow, glasses rim, and cheek unless explicitly requested.
6. **Match geometry, not merely content.** The corrected eye must match the reference eye's visible aperture, lid contour, sclera exposure, iris diameter, gaze direction, and perspective. A mirrored eye at the wrong scale is a failed edit.
7. **Blend conservatively.** Use a tight feathered mask. Preserve the original frame of glasses and local illumination; avoid broad low-opacity overlays that leave a double eyelid or duplicate sclera.
8. **Verify before delivery.** Compare both eyes in a tight crop and at full-image scale. Check for enlargement, mismatch, seams, blur, doubled pupils/lids, unequal sclera, frame distortion, and altered identity.
9. **Deliver one clearly versioned output.** If revising after feedback, say what was corrected and provide the new file, not the rejected version.

## Eye-correction acceptance criteria

- Correct anatomical eye was edited.
- Visible eye widths and heights match within natural perspective.
- Upper and lower lid curvature correspond.
- Iris/pupil size and gaze direction are consistent.
- Visible sclera is balanced as requested.
- No eye is perceptibly enlarged.
- Glasses, eyebrows, face outline, and skin texture are unchanged.
- No seam, halo, blur patch, duplication, or color discontinuity is visible.
- Full portrait remains natural at normal viewing size.

## Revision discipline

When the user reports that an eye is too large or differs from the other:

1. accept the correction directly;
2. return to the original image;
3. re-check anatomical left/right;
4. reduce the edit region to the actual eye aperture;
5. match source and target eye dimensions numerically before compositing;
6. use stronger replacement inside the eye and feather only the perimeter;
7. verify both eye geometry and sclera exposure before sending.

Do not trust a generic “looks natural” assessment when the user's requirement is bilateral equality. Explicitly evaluate the named attributes.

## Supporting reference

See `references/eye-matching-checklist.md` for a deterministic eye-retouching checklist and coordinate conventions.
