## running the game

```sh
git clone https://github.com/rsa17826/mq.git
cd mq
direnv allow
./generate_map_scales.sh

python desktop_app.py
```

## images

<!-- ![](./gh_images/screenshot_20260706_193750_391.png) -->

![](./gh_images/screenshot_20260706_193756_529.png)
![](./gh_images/screenshot_20260706_193500_442.png)
![](./gh_images/screenshot_20260706_193455_244.png)
![](./gh_images/screenshot_20260706_193505_620.png)
![](./gh_images/screenshot_20260706_193408_682.png)
![](./gh_images/screenshot_20260706_193515_978.png)

## tips or other notes

lower key repeat delay increases enemy encounters

`20_23` red chest has best slamstone droprates as it waw coded incorrectly

```js
} else if (this.prize >= 10) {
  this.prize = Math.ceil(rng.random() * 50) + 10
  newObserveObject.fightMes[
    newObserveObject.fightMesCurrent
  ].set_text(
    "You find " +
      this.prize +
      " bear claws in the chest.",
  )
  manager.slamstones += this.prize
} else {
```

fastest way to force another encounter is quickly tapping any arrow key - shown by `manager.tap`

