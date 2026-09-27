# AR0234 USB Camera Worked Case

Session date: 2026-08-17. This is a worked example, not a live price baseline. Re-fetch every offer before procurement.

## Target

USB 3.0 camera module; global shutter; approximately 2 MP; 1920×1080 at 120 fps; MJPG, YUY2, and H.264; fixed-focus lens around 100°.

## Identification

The distinctive combination points to the onsemi AR0234CS family. The official sensor page states a 1920×1200 active array, global shutter, and 120 fps at full sensor resolution:

- https://www.onsemi.com/products/sensors/image-sensors/ar0234cs

This is a sensor capability, not proof that every USB module exposes 1920×1080 at 120 fps.

## Decisive Contradiction

e-con Systems' documented See3CAM_24CUG uses AR0234CS and advertises a high-frame-rate USB camera, but its specification table distinguishes:

- HD at 120 fps;
- Full HD at 60 fps;
- MJPEG and uncompressed UYVY;
- no H.264 claim;
- 104.6° horizontal FOV with its supplied lens;
- public sample price starting at USD 99 excluding shipment.

Source:
https://www.e-consystems.com/industrial-cameras/ar0234-usb3-global-shutter-camera.asp

This demonstrates why `sensor supports 120 fps` must not be promoted to `finished USB module supports Full HD 120 fps` without a mode table.

## Offer Patterns Observed

A marketplace search exposed an exact-title offer claiming 1920×1080/120, USB3, MJPG/YUY2/H.264 at USD 111.17, with visible 5.0 and 8 sold. The retrieved public view did not expose the merchant name or verify the 100° lens variant.

Other offers mixed:

- 1920×1200/120 with 130° lens;
- ELP-branded 1080p/120 without visible codec/FOV details;
- trigger-capable variants with incomplete resolution/codec evidence;
- 90 fps ELP manufacturer variants;
- B2B modules with low unit prices but MOQ and unconfirmed USB/H.264 interfaces.

Marketplace source used for discovery:
https://www.aliexpress.com/w/wholesale-ar0234-usb-camera.html

## Strong Documented Alternatives

- **e-con See3CAM_24CUG:** strongest documentation and procurement confidence, but Full HD 60 fps and no H.264.
- **Arducam B0495:** public USD 139.99, AR0234 USB3 global shutter, YUYV and 95° diagonal lens; advertised high-frame-rate mode was up to 80 fps at 960×600, so it is not an exact substitute.
- **ELP ELP-USBGS1200P01-V100:** official page showed 1080P/1200P at 90 fps and `$0.00`, interpreted as request for quote rather than a free product.

## Recommended Procurement Test

For the exact marketplace offer, require all of the following before ordering more than one sample:

1. `v4l2-ctl --list-formats-ext` or USB Device Tree Viewer output.
2. A mode showing 1920×1080 at 120 fps for each required format.
3. Short original H.264 and MJPEG sample files with ffprobe/MediaInfo output.
4. Lens model and FOV explicitly identified as horizontal/diagonal/vertical.
5. Firmware version, sensor model, USB bridge/ISP, OS support, and return terms.

## Scoring Lesson

Keep two conclusions side by side:

- **best exact-title match** may be a marketplace offer with weaker evidence;
- **lowest procurement risk** may be a documented industrial camera that misses one or more must-haves.

Do not collapse these into a single winner without showing must-have failures.