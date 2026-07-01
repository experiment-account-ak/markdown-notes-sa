# JavaScript State

State is the data that describes the current condition of an interface.

```js
const state = {
  currentSlide: 0,
  theme: "light",
  searchQuery: ""
};
```

When state changes, the relevant part of the interface should update.

---

# Fetching Local Files

The app loads Markdown files with `fetch()`:

```js
const response = await fetch("notes/01-introduction.md");

if (!response.ok) {
  throw new Error("The note could not be loaded.");
}

const markdown = await response.text();
```

This is why the project must run through a localhost web server.

---

# Keyboard Navigation

A small event listener can support presentation-style controls.

```js
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    showNextSlide();
  }

  if (event.key === "ArrowLeft") {
    showPreviousSlide();
  }
});
```

Useful additions include:

1. Ignoring shortcuts while the user is typing
2. Supporting `Home` and `End`
3. Preventing navigation beyond the first or last slide
