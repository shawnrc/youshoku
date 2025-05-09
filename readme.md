# yōshoku
- [ ] conversionprofile reference schema
- [ ] inheritance scheme for cameras
    - [x] x100v
    - [ ] x-pro3
    - [ ] whatever else i can get my hands on
- [x] fxw to fp1 conversion tool
- [ ] recipe manager

## Things I should mention

### DR and DR-P cannot be set to auto in a Conversion Profile

This sort of makes sense because when either dynamic range setting is set to
auto, the camera picks a DR value based on current lighting conditions. When
applying recipes post-hoc, the camera obviously can't accurately judge what the
lighting conditions were at the time, so "auto" maybe doesn't make a whole lot
of sense.

That said, I don't see why it can't be used as a setting for two uses:
- Setting DR/DR-P to Auto when sending settings to the camera
- Picking the widest range possible based on what the camera originally selected
  when taking the photo

#### What does this mean for users?

After transferring recipes to your camera, any recipe that uses DR-Auto or DR-P
Auto needs to be manually corrected. It's not clear to me what value should be
written to a profile (either 100 for the weakest effect or 400 for the
strongest), so this should be a toggleable when converting from PKL to FP1.

(I think 100 might be better because I'd rather err towards a wider dynamic
range than a narrower one that might unintuively look washed out).

### Dynamic Range, D Range Priority, and HDR

All three of these settings are mutually-exclusive. HDR even turns off other
features. DR can't be turned off, so DR-P takes precedence over DR, and HDR
technically takes precedence over both, but can't really be used in recipes
anyhow because it's a drive mode rather than an IQ setting.

### Unsupported devices

X Raw Studio only works with X-Trans III-era cameras and newer. I was very
disappointed when I tried plugging my X-Pro1 in to no avail.

### Exposure compensation

There's an implicit convention that FujiXWeekly set where recipes come with a
recommended exposure compensation range, but this is *not* the same as exposure
bias in a conversion profile. `ExposureBias` is used for push/pull processing
and might not look great with all images.
